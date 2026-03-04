document.addEventListener('DOMContentLoaded', () => {
    const searchbar = document.getElementById('searchbar');
    const suggestionBox = document.querySelector('.suggestions');

    searchbar.onkeyup = async function() {
        let query = searchbar.value.trim();

        if (query.length > 2) {
            try {
                const response = await fetch('/autocomplete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ "query": query })
                }); 

                const suggestions = await response.json();
                
                display(suggestions, suggestionBox);

            } catch (error) {
                console.error("Search failed:", error);
            }
        } else {
            suggestionBox.innerHTML = "";
        }
    };

    searchbar.addEventListener('blur', () => {
        setTimeout(() => {
            suggestionBox.style.display = 'none';
        }, 200);
    });

    searchbar.addEventListener('focus', () => {
        if (searchbar.value.trim().length > 2) {
            suggestionBox.style.display = 'block';
        }
    });
});

function display(suggestions, container) {
    container.innerHTML = "";
    
    if (!suggestions || suggestions.length === 0) {
        container.style.display = 'none';
        return;
    }

    const ul = document.createElement('ul');

    //Loop through results and create clickable items
    suggestions.forEach((item) => {
        const li = document.createElement('li');
        li.textContent = item;
        
        li.onclick = function() {
            const searchbar = document.getElementById('searchbar');
            
            //Set the search bar text to the clicked item
            searchbar.value = item; 
            
            container.innerHTML = "";
            container.style.display = 'none';
            
            //Automatically submit the form after clicking
            //searchbar.closest('form').submit();
        };

        ul.appendChild(li);
    });

    container.appendChild(ul);
    container.style.display = 'block';
}