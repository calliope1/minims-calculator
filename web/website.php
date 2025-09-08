<!DOCTYPE html>
<html>
<head>

<title>Minims calculator</title>

<!-- Add meta and head if you want -->

</head>

<body id="body">

<!-- Add headers if you want -->

<main id="main">

<p>
  To use this tool, write your expression, replacing each minim with a vertical bar |.<br>
  Alternatively, you can wirte numbers, which will be interpreted as that many minims.<br>
  <b>Example:</b> '3TA||R' will return every work that can be made from three minims followed by the letters TA, two further minims and finally the letter R.
</p>

<input type="text" id="minims" placeholder="Enter minims computation string">
<button id="computeButton">Compute</button>

<div id="results">Results will appear here...</div>

  <script>
    const endpoint = "https://example.com/api/compute"; // Replace with your actual endpoint

    const button = document.getElementById("computeButton");
    const resultsDiv = document.getElementById("results");

    button.addEventListener("click", async () => {
      const query = document.getElementById("minims").value.trim();

      if (!query) {
        resultsDiv.textContent = "Enter a string.";
        return;
      }

      try {
        const getPoint = `${endpoint}?expression=${encodeURIComponent(query)}`;

        const response = await fetch(getPoint);
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();

        // Display only the "results" part
        if (data.results) {
          resultsDiv.textContent = data.results.join(', ');
        } else {
          resultsDiv.textContent = "No results found in response.";
        }
      } catch (error) {
        resultsDiv.textContent = "Error: " + error.message;
      }
    });
  </script>

</main>

</body>
</html>
