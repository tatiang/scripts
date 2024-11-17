// Web Viewer script to listen for messages
window.addEventListener("message", (event) => {
    try {
        const data = JSON.parse(event.data); // Parse the incoming JSON message

        if (data.action === "checkDay") {
            // Extract the date from the message
            const date = data.date;
            const result = checkDayThunkable(date); // Call the function
            // Send the result back to Thunkable
            window.ReactNativeWebView.postMessage(JSON.stringify({ result }));
        }
    } catch (error) {
        // Handle any errors
        window.ReactNativeWebView.postMessage(
            JSON.stringify({ error: "Invalid message format or unexpected error" })
        );
    }
});

// Check Day Function
function checkDayThunkable(date) {
    try {
        const inputDate = new Date(date);
        if (isNaN(inputDate)) {
            return "Error: Invalid date format. Use 'Mth Day, Year' (e.g., 'Nov 16, 2024').";
        }

        const dayOfWeek = inputDate.getDay();
        const formattedDate = inputDate.toISOString().split("T")[0];

        const holidays = [
            "2024-01-01", // New Year's Day
            "2024-01-15", // Martin Luther King Jr. Day
            "2024-02-19", // Presidents' Day
            "2024-05-27", // Memorial Day
            "2024-07-04", // Independence Day
            "2024-09-02", // Labor Day
            "2024-11-11", // Veterans Day
            "2024-11-28", // Thanksgiving Day
            "2024-12-25"  // Christmas Day
        ];

        if (holidays.includes(formattedDate)) {
            return "Holiday";
        }

        if (dayOfWeek === 0 || dayOfWeek === 6) {
            return "Weekend";
        }

        return "Weekday";
    } catch (error) {
        return `Error: ${error.message}`;
    }
}
