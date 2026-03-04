// We wait for the page to load, then find our elements
document.addEventListener('DOMContentLoaded', () => {
    const searchbar = document.getElementById('searchbar');
    const suggestionBox = document.querySelector('.suggestions');

    searchbar.onkeyup = async function() {
        let query = searchbar.value.trim();

        if (query.length > 2) {
            try {
                const response = await fetch('/live-search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ "query": query })
            }); 
            
            const suggestions = await response.json();
            display(suggestions)
            }
            catch {console.error('oh no')}
        }
        
        else {
            suggestionBox.innerHTML ='yolo'
        }
    };
});

function display(suggestions) {
    const content = suggestions.map((list)=>{
        return "<li>" + list + "</li>"
    });

    suggestionBox.innerHTML = "<ul>" + content + "</ul>"
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
