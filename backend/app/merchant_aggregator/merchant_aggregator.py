import os
from datetime import datetime
from multiprocessing import Process, Queue
from app.database.models import Transaction, UserParsedCategory, db
from app.helper import get_prompt_template, query_chatgpt
from app.logger import log
from app.merchant_aggregator.utils import (
    _serialize_transactions,
    _split_into_chunks,
    _extract_merchant_from_transaction,
    _has_timed_out,
    _get_categories_from_chatgpt_response,
    _retrieve_cached_categories,
    _get_user_categories_dict,
)

APP_NAME = "Merchant Aggregator"


def _categorize_chunk(chunk, user_categories_dict, user_email, queue):
    """Categorizes a chunk of transactions using ChatGPT"""

    log(APP_NAME, "DEBUG", f"Categorizing chunk of size: {len(chunk)} (PID: {os.getpid()})")

    categories_string = ",".join(user_categories_dict.keys())
    transactions_string = "\n".join(
        [f'"{_extract_merchant_from_transaction(transaction["merchantData"]["name"])}"' for transaction in chunk]
    )
    prompt = get_prompt_template(categories_string, transactions_string)
    chatgpt_response = query_chatgpt(prompt)

    generated_categories = _get_categories_from_chatgpt_response(chatgpt_response)
    parsed_categories = []

    for index in range(len(generated_categories)):
        category = generated_categories[index]

        if index >= len(chunk):
            log(
                APP_NAME,
                "WARNING",
                f"Generated categories count is larger than the chunk size -> {len(generated_categories)} / {len(chunk)}",
            )
            break

        if "Category for" in category:
            category_name = category.split(": ")[1].strip()

            if category_name in user_categories_dict:
                category_id = user_categories_dict[category_name]["id"]
                custom_category = user_categories_dict[category_name]["is_custom"]

                # Update transaction category
                chunk[index]["categoryId"] = category_id

                # Update cached categories
                parsed_categories.append(
                    UserParsedCategory(
                        chargingBusiness=chunk[index]["merchantData"]["name"],
                        targetCategoryId=category_id,
                        userEmail=user_email if custom_category else None,
                    )
                )
            else:
                log(
                    APP_NAME,
                    "WARNING",
                    f"Generated unrecognized category: '{category_name}' for transaction: {chunk[index]['merchantData']['name']}",
                )
    queue.put((chunk, parsed_categories))


def _process_chunk(chunks, user_categories, processing_data):
    """Processes a set of transaction chunks in parallel while verifying each process's timeout."""

    timeout = processing_data["timeout"]
    user_email = processing_data["user_email"]
    processes = []
    process_results = [None] * len(chunks)

    log(APP_NAME, "DEBUG", f"Starting to process {len(chunks)} chunks in parallel.")

    for index, chunk in enumerate(chunks):
        q = Queue()
        p = Process(target=_categorize_chunk, args=(chunk, user_categories, user_email, q))
        p.start()
        processes.append({"process": p, "queue": q, "index": index, "size": len(chunk)})

    start_time = datetime.now()

    while not _has_timed_out(start_time, timeout):
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


def _process_data_in_chunks(transactions, user_categories, processing_data):
    """Splits transactions into chunks and processes them in parallel batches"""

    if len(transactions) == 0:
        return {"transactions": [], "user_parsed_categories": []}

    chunk_size = processing_data["chunk_size"]
    parallel_count = processing_data["parallel_count"]

    chunks = _split_into_chunks(transactions, chunk_size)
    current_chunk_index = 0

    while current_chunk_index < len(chunks):
        batch = []

        for _ in range(parallel_count):
            if current_chunk_index < len(chunks):
                batch.append(chunks[current_chunk_index])
                current_chunk_index += 1

        batch_results = _process_chunk(batch, user_categories, processing_data)
        results = {"transactions": [], "user_parsed_categories": []}

        for chunk_result in batch_results:
            if chunk_result is None:
                continue
            user_parsed_transactions = chunk_result[0]
            user_parsed_categories = chunk_result[1]

            results["transactions"].extend(user_parsed_transactions)
            results["user_parsed_categories"].extend(user_parsed_categories)

            yield results


def categorize_for_all_users(user_transactions_dict):
    """
    Processes and categorizes transactions for multiple users.
    Uses the UserParsedCategory table to parse previously parsed transactions with cache.
    Uses ChatGPT for uncached transactions.

    Args:
        user_transactions_dict (dict): A dictionary where keys are user emails and values are lists of transaction objects.

    Returns:
        tuple: A tuple containing two elements:
               1. A list of dictionaries, each containing 'id' and 'categoryId' of processed transactions.
               2. A list of user parsed categories.
    """

    user_parsed_categories = []
    parsed_transactions = []
    processed_transactions = []

    # Iterate over each user and their transactions
    for email, transactions in user_transactions_dict.items():
        if not transactions:
            log(APP_NAME, "INFO", f"No transactions to categorize for user {email}")
            continue

        log(APP_NAME, "INFO", f"Categorizing transactions for user {email}, total transactions {len(transactions)}")

        # Retrieve user-specific categories and cached categories
        user_categories = _get_user_categories_dict(email)
        cached_merchants_mapping = _retrieve_cached_categories(email)
        cached_transactions = []
        transactions_to_process = []

        # Iterate over each transaction for the user
        for t in _serialize_transactions(transactions):
            # Extract the merchant name from the transaction data
            merchant_name = _extract_merchant_from_transaction(t["merchantData"]["name"])
            cached_value = cached_merchants_mapping.get(merchant_name, None)

            # If there's a cached category for the merchant, use it and remove the transaction from processing
            if cached_value is not None:
                t["categoryId"] = cached_value
                cached_transactions.append(t)
            else:
                transactions_to_process.append(t)

        log(APP_NAME, "DEBUG", f"Found {len(cached_transactions)} transactions with cached merchants")

        # Set up processing data for chunk processing
        processing_data = {"timeout": 30, "chunk_size": 8, "parallel_count": 20, "user_email": email}

        log(
            APP_NAME,
            "DEBUG",
            f"Processing data in chunks. Unchached transactions: {len(transactions_to_process)}, processing_data: {processing_data}",
        )
        processed_transactions.extend(cached_transactions)

        for results in _process_data_in_chunks(transactions_to_process, user_categories, processing_data):
            processed_transactions = results["transactions"]
            user_parsed_categories.extend(results["user_parsed_categories"])

            # Prepare transactions for commit
            parsed_transactions_batch = [
                {"id": t["id"], "categoryId": t["categoryId"]} for t in processed_transactions if t is not None
            ]
            parsed_transactions.extend(parsed_transactions_batch)

            # Commit batch to database
            db.session.bulk_update_mappings(Transaction, parsed_transactions_batch)
            db.session.add_all(user_parsed_categories)
            db.session.commit()

            # Clear lists for next batch
            parsed_transactions_batch.clear()
            user_parsed_categories.clear()
            processed_transactions.clear()

        # Log the completion of categorization for a user
        log(
            APP_NAME,
            "INFO",
            f"Finished categorizing transactions for user {email}, processed {len(processed_transactions)} new transactions",
        )
    return (parsed_transactions, user_parsed_categories)
