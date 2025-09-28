async function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const statusDiv = document.getElementById("uploadStatus");

  if (!fileInput.files.length) {
    statusDiv.innerText = "⚠️ Please select a file first.";
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const response = await fetch("/api/upload", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Upload failed");
    const result = await response.json();

    statusDiv.innerText = "✅ Upload successful!";
  } catch (error) {
    statusDiv.innerText = "❌ Upload failed: " + error.message;
  }
}

async function askQuery() {
  const query = document.getElementById("queryInput").value;
  const resultsDiv = document.getElementById("results");

  if (!query) {
    resultsDiv.innerHTML = `<p class="text-red-600">⚠️ Please enter a query.</p>`;
    return;
  }

  resultsDiv.innerHTML = `<p class="text-gray-500">⏳ Searching...</p>`;

  try {
    const response = await fetch(`/api/ask?query=${encodeURIComponent(query)}`);
    if (!response.ok) throw new Error("Query failed");
    const result = await response.json();

    resultsDiv.innerHTML = `
      <div class="p-4 bg-gray-100 rounded">
        <h3 class="font-semibold mb-2">Answer:</h3>
        <p class="mb-4">${result.answer || "No answer found."}</p>

        <h4 class="font-semibold mb-1">Compliance Check:</h4>
        <ul class="list-disc list-inside text-sm text-gray-700">
          ${(result.compliance || [])
            .map(rule => `<li>${rule.rule}: ${rule.status ? "✅" : "❌"}</li>`)
            .join("")}
        </ul>
      </div>
    `;
  } catch (error) {
    resultsDiv.innerHTML = `<p class="text-red-600">❌ Error: ${error.message}</p>`;
  }
}
