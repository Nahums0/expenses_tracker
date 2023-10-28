from datetime import datetime
from multiprocessing import Process, Queue
from app.database.models import UserParsedCategory, db
from app.helper import get_prompt_template, query_chatgpt
from app.logger import log
from app.merchant_aggregator.utils import (
    _split_into_chunks,
    extract_merchant_from_transaction,
    has_timed_out,
    get_categories_from_chatgpt_response,
    retrieve_cached_categories,
    get_user_categories_dict,
)
import os

APP_NAME = "Merchant Aggregator"


def _categorize_chunk(chunk, user_categories_dict, queue):
    """Categorizes a chunk of transactions using ChatGPT"""

    log(APP_NAME, "DEBUG", f"Categorizing chunk of size: {len(chunk)} (PID: {os.getpid()})")

    categories_string = ",".join(user_categories_dict.keys())
    transactions_string = "\n".join(
        [
            f'"{extract_merchant_from_transaction(transaction.merchantData["name"])}"'
            for transaction in chunk
        ]
    )
    prompt = get_prompt_template(categories_string, transactions_string)
    chatgpt_response = query_chatgpt(prompt)

    generated_categories = get_categories_from_chatgpt_response(chatgpt_response)
    parsed_categories = []

    for index in range(len(generated_categories)):
        category = generated_categories[index]

        if index >= len(chunk):
            log(APP_NAME, "WARNING", f"Generated categories count is larger than the chunk size -> {len(generated_categories)} / {len(chunk)} ")
            break

        if "Category for" in category:
            category_name = category.split(": ")[1].strip()

            if category_name in user_categories_dict:
                category_id = user_categories_dict[category_name]["id"]
                custom_category = user_categories_dict[category_name]["is_custom"]

                # Update transaction category
                chunk[index].categoryId = category_id

                # Update cached categories if it's not custom for user
                if not custom_category:
                    parsed_categories.append(UserParsedCategory(
                        chargingBusiness=chunk[index].merchantData["name"],
                        targetCategoryId=category_id,
                        userEmail=None
                    ))
            else:
                log(APP_NAME, "WARNING", f"Generated unrecognized category: '{category_name}' for transaction: {chunk[index].merchantData['name']}")
    queue.put((chunk, parsed_categories))


def _process_chunk(chunks, user_categories, timeout):
    """Processes a set of transaction chunks in parallel while verifying each process's timeout."""

    processes = []
    process_results = [None] * len(chunks)

    log(APP_NAME, "DEBUG", f"Starting to process {len(chunks)} chunks in parallel.")

    for index, chunk in enumerate(chunks):
        q = Queue()
        p = Process(target=_categorize_chunk, args=(chunk, user_categories, q))
        p.start()
        processes.append({"process": p, "queue": q, "index": index, "size": len(chunk)})

    start_time = datetime.now()

    while not has_timed_out(start_time, timeout):
        active_processes = [p for p in processes if p["process"].is_alive()]
        if not active_processes:
            break

    completed_count = 0
    for proc_info in processes:
        proc = proc_info["process"]
        queue = proc_info["queue"]
        chunk_index = proc_info["index"]
        result = None

        if not proc.is_alive():
            result = queue.get()
            completed_count += 1
        else:
            proc.terminate()
            result = None
            log(APP_NAME, "WARNING", f"Terminated process {proc.pid}, reached timeout")

        process_results[chunk_index] = result

    log(APP_NAME, "DEBUG", f"Processed {completed_count} out of {len(chunks)}")
    return process_results


def process_data_in_chunks(transactions, user_categories, timeout, chunk_size, parallel_count):
    """Splits transactions into chunks and processes them in parallel batches"""

    chunks = _split_into_chunks(transactions, chunk_size)
    results = {"transactions":[], "user_parsed_categories":[]}
    current_chunk_index = 0

    while current_chunk_index < len(chunks):
        batch = []

        for _ in range(parallel_count):
            if current_chunk_index < len(chunks):
                batch.append(chunks[current_chunk_index])
                current_chunk_index += 1

        batch_results = _process_chunk(batch, user_categories, timeout)

        for chunk_result in batch_results:
            if chunk_result is None:
                continue
            user_parsed_transactions = chunk_result[0]
            user_parsed_categories = chunk_result[1]

            for t in user_parsed_transactions:
                results["transactions"].append(t)

            for c in user_parsed_categories:
                results["user_parsed_categories"].append(c)

    return results

def categorize_for_all_users(user_transactions_dict):
    """Processes and categorizes transactions for multiple users.
    Uses the UserParsedCategory tabled to parse previously parsed transactions with cache
    Uses ChatGPT for uncached transactions."""

    user_parsed_categories = []
    parsed_transactions = []

    for email, transactions in user_transactions_dict.items():
        if transactions:
            log(APP_NAME, "INFO", f"Categorizing transactions for user {email}, total transactions {len(transactions)}")
            user_categories = get_user_categories_dict(email)
            cached_merchants_mapping = retrieve_cached_categories(email)
            cached_transactions = []

            for t in transactions:
                merchant_name = extract_merchant_from_transaction(t.merchantData["name"])
                cached_value = cached_merchants_mapping.get(merchant_name, None)
                if cached_value is not None:
                    t.categoryId = cached_value
                    transactions.remove(t)
                    cached_transactions.append(t)

            log(APP_NAME, "DEBUG", f"Found {len(cached_transactions)} transactions with cached merchants")

            timeout = 60
            chunk_size = 8
            parallel_count = 20

            log(APP_NAME, "DEBUG", f"Processing data in chunks. Unchached transactions: {len(transactions)}, timeout: {timeout}, chunk size: {chunk_size}, parallel count: {parallel_count}")

            results = process_data_in_chunks(transactions, user_categories, timeout, chunk_size, parallel_count)

            processed_transactions = results["transactions"]
            processed_transactions.extend(cached_transactions)
            user_parsed_categories.extend(results["user_parsed_categories"])

            parsed_transactions.extend([{"id": t.id, "categoryId": t.categoryId} for t in processed_transactions if t is not None])
            log(APP_NAME, "INFO", f"Finished categorizing transactions for user {email}, processed {len(processed_transactions)} new transactions")
        else:
            log(APP_NAME, "INFO", f"No transactions to categorize for user {email}")
    return (parsed_transactions, user_parsed_categories)
