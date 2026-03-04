document.addEventListener('DOMContentLoaded', () => {
    const searchbar = document.getElementById('searchbar');
    const suggestionBox = document.querySelector('.suggestions');

    searchbar.onkeyup = async function() {
        // .trim() removes whitespace from both ends
        let query = searchbar.value.trim();

        // Only search if we have at least 3 characters
        if (query.length > 2) {
            try {
                const response = await fetch('/live-search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ "query": query })
                }); 

                // We define 'suggestions' HERE so it can see 'response'
                const suggestions = await response.json();
                
                // Pass the data to your display function
                display(suggestions, suggestionBox);

            } catch (error) {
                console.error("Search failed:", error);
            }
        } else {
            // Clear suggestions if the input is too short
            suggestionBox.innerHTML = "";
        }
    };
});

// container is passed in so this function knows where to put the HTML
function display(suggestions, container) {
    if (!suggestions || suggestions.length === 0) {
        container.innerHTML = "<ul><li>No results found</li></ul>";
        return;
    }

    const htmlContent = suggestions.map((item) => {
        // Wrap each result in a list item
        return `<li>${item}</li>`;
    }).join(''); // join('') removes the commas between array items

    container.innerHTML = `<ul>${htmlContent}</ul>`;
}
//     // Only search if the user typed more than 2 letters
//     if (query.length > 2) {
//         const response = await fetch('/live-search', {
//             method: 'POST',
//             headers: {'Content-Type': 'application/json'},
//             body: JSON.stringify({ query: query })
//         });

//         const results = await response.json();
//         displayResults(results);
//     } else {
//         // Clear suggestions if the input is too short
//         suggestionBox.innerHTML = "Suggestions will appear here";
//     }
// };

// function displayResults(results) {
//     if (!results.length) {
//         suggestionBox.innerHTML = "";
//         return;
//     }

//     // Build the list items based on what Flask/Wikipedia sent back
//     const htmlRows = results.map((item) => {
//         return `<li><a href="/graph/?page=${encodeURIComponent(item)}">${item}</a></li>`;
//     });

//     // Inject the <ul> into your suggestions div
//     suggestionBox.innerHTML = `<ul>${htmlRows.join('')}</ul>`;
// }
// });

// function togglesidebar() {
// const wrapper = document.querySelector(".wrapper");   
// if (wrapper) {
//     wrapper.classList.toggle("sidebar_open");
// } else {
//     console.error("Error: Could not find the .wrapper element");
// }
// }
