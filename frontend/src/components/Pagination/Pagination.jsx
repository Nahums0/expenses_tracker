const PagePicker = ({ totalPages, currentPage, setCurrentPage, setPageSize, className }) => {
  const lookoutCount = 3;

  // Calculate the start and end pages for pagination
  let startPage = currentPage - lookoutCount > 0 ? currentPage - lookoutCount : 1;
  let endPage = currentPage + lookoutCount < totalPages ? currentPage + lookoutCount : totalPages;

  const handleJumpToPage = (event) => {
    if (event.target.value < 0) {
      console.log(event.target.value);
      event.stopPropagation;
      return;
    }
    const page = Number(event.target.value);
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  return (
    <div
      className={`${className} flex flex-wrap justify-center lg:justify-between pl-5 pr-5 items-center space-x-2 w-full`}
    >
      {/* Jump to Page Input */}
      <div className="flex-row items-center hidden lg:flex">
        <label htmlFor="jump-to-page" className="text-lg mb-1">
          Go to page:
        </label>
        <input
          id="jump-to-page"
          type="number"
          className="text-lg pt-2 pb-2 border rounded w-12 text-center ml-3"
          placeholder="#"
          onChange={handleJumpToPage}
          onBlur={(e) => {
            e.target.value = currentPage;
          }}
        />
      </div>

      <div className="flex flex-row">
        {/* Go to First Page */}
        {currentPage > 1 && (
          <button onClick={() => setCurrentPage(1)} className="text-lg p-2 text-gray-400">
            &lt;&lt;
          </button>
        )}

        {/* Previous Button */}
        {currentPage > 1 && (
          <button onClick={() => setCurrentPage(currentPage - 1)} className="text-lg p-2 text-gray-400">
            &lt;
          </button>
        )}

        {/* Page Numbers */}
        {Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i).map((page) => (
          <div
            key={page}
            onClick={() => setCurrentPage(page)}
            className={`cursor-pointer text-lg p-2 text-gray-400 flex justify-center items-center ${
              page === currentPage && "bg-blue-500 rounded-full text-white mt-[4px]"
            }`}
            style={{
              width: page === currentPage ? "35px" : "auto",
              height: page === currentPage ? "35px" : "auto",
            }}
          >
            {page}
          </div>
        ))}

        {/* Next Button */}
        {currentPage < totalPages && (
          <button onClick={() => setCurrentPage(currentPage + 1)} className="text-lg p-2 text-gray-400">
            &gt;
          </button>
        )}

        {/* Go to Last Page */}
        {currentPage < totalPages && (
          <button onClick={() => setCurrentPage(totalPages)} className="text-lg p-2 text-gray-400">
            &gt;&gt;
          </button>
        )}
      </div>

      {/* Page Size Selector */}
      <div className="hidden lg:flex flex-row items-center">
        <label htmlFor="page-size" className="text-lg mb-1">
          Items per page:
        </label>
        <select id="page-size" className="text-lg p-2 border rounded" onChange={setPageSize}>
          {[10, 20, 30, 50, 100].map((size) => (
            <option key={size} value={size}>
              {size}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default PagePicker;
