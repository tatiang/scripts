// Listener to handle messages from Thunkable
window.addEventListener("message", (event) => {
    console.log("Received message:", event.data); // Log the received message for debugging

    try {
        // Parse the incoming JSON message
        const data = JSON.parse(event.data);

        // Check for the 'checkDay' action
        if (data.action === "checkDay") {
            console.log("Action: checkDay"); // Log the action for debugging

            // Extract the date from the message
            const date = data.date;
            console.log("Date received:", date); // Log the date for debugging

            // Call the function to process the date
            const result = checkDayThunkable(date);

            // Log the result for debugging
            console.log("Result:", result);

            // Send the result back to Thunkable
            window.ReactNativeWebView.postMessage(JSON.stringify({ result }));
        } else {
            // Handle unexpected actions
            console.error("Unknown action:", data.action);
            window.ReactNativeWebView.postMessage(
                JSON.stringify({ error: "Unknown action" })
            );
        }
    } catch (error) {
        // Log the error for debugging
        console.error("Error processing message:", error.message);

        // Send the error back to Thunkable
        window.ReactNativeWebView.postMessage(
            JSON.stringify({ error: "Invalid message format or unexpected error" })
        );
    }
});

// Function to check if the given date is a Holiday, Weekend, or Weekday
function checkDayThunkable(date) {
    try {
        const inputDate = new Date(date);
        if (isNaN(inputDate)) {
            console.error("Invalid date format:", date); // Log invalid date for debugging
            return "Error: Invalid date format. Use 'Mth Day, Year' (e.g., 'Nov 16, 2024').";
        }

        // Get the day of the week (0 = Sunday, 1 = Monday, ..., 6 = Saturday)
        const dayOfWeek = inputDate.getDay();

        // Format the date as 'YYYY-MM-DD'
        const formattedDate = inputDate.toISOString().split("T")[0];

        console.log("Formatted date:", formattedDate); // Log the formatted date for debugging

        // Common U.S. holidays (hardcoded)
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

        // Check if the date is a holiday
        if (holidays.includes(formattedDate)) {
            console.log("Holiday detected:", formattedDate); // Log holiday detection
            return "Holiday";
        }

        // Check if the date is a weekend
        if (dayOfWeek === 0 || dayOfWeek === 6) {
            console.log("Weekend detected:", formattedDate); // Log weekend detection
            return "Weekend";
        }

        // Otherwise, it's a weekday
        console.log("Weekday detected:", formattedDate); // Log weekday detection
        return "Weekday";
    } catch (error) {
        // Log unexpected errors
        console.error("Error in checkDayThunkable function:", error.message);
        return `Error: ${error.message}`;
    }
}
