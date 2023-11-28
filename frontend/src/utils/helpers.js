export function numberWithCommas(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

export function getFirstOfNearestMonth(format = "dd-mm-yyyy") {
  var currentDate = new Date();
  var currentDay = currentDate.getDate();
  var currentMonth = currentDate.getMonth();
  var currentYear = currentDate.getFullYear();

  // If today is not the first day of the month, move to the next month
  if (currentDay !== 1) {
    // If the current month is December, move to January of the next year
    if (currentMonth === 11) {
      currentYear++;
      currentMonth = 0;
    } else {
      currentMonth++;
    }
  }

  var firstDay = new Date(currentYear, currentMonth, 1);
  return formatDate(firstDay, format);
}

export function formatDate(date, format) {
  var year = date.getFullYear();
  var month = (date.getMonth() + 1).toString().padStart(2, "0");
  var day = date.getDate().toString().padStart(2, "0");

  return format.replace("yyyy", year).replace("mm", month).replace("dd", day);
}

export function getCurrencySymbol(currencyName) {
  const currencySymbols = {
    USD: "$",
    ILS: "₪",
    EUR: "€",
    JPY: "¥",
    GBP: "£",
    AUD: "A$",
    CAD: "C$",
    CHF: "CHF",
    CNY: "¥",
    SEK: "kr",
    NZD: "NZ$",
    MXN: "$",
    SGD: "S$",
    HKD: "HK$",
    NOK: "kr",
    KRW: "₩",
    TRY: "₺",
    RUB: "₽",
    INR: "₹",
    BRL: "R$",
    ZAR: "R",
    THB: "฿",
  };

  currencyName = currencyName.toUpperCase(); // Convert to uppercase for case-insensitive matching
  return currencySymbols[currencyName] || currencyName; // Return the symbol or the original name if not found
}
