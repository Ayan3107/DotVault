const API_URL = "";

const itemsContainer = document.getElementById("itemsContainer");
const searchInput = document.getElementById("searchInput");
const filters = document.querySelectorAll(".filter");

const addButton = document.getElementById("addButton");
const modal = document.getElementById("modal");
const closeModal = document.getElementById("closeModal");
const itemForm = document.getElementById("itemForm");

const titleInput = document.getElementById("titleInput");
const contentInput = document.getElementById("contentInput");
const categoryInput = document.getElementById("categoryInput");
const tagsInput = document.getElementById("tagsInput");

let currentCategory = "all";
let searchTimeout;


/* ---------------------------------------------------------
   LOAD ITEMS
--------------------------------------------------------- */

async function loadItems() {
    try {
        const response = await fetch(`${API_URL}/items`);

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to load items");
        }

        displayItems(data);

    } catch (error) {
        console.error("Load error:", error);

        itemsContainer.innerHTML = `
            <div class="empty">
                Could not load your vault.
            </div>
        `;
    }
}


/* ---------------------------------------------------------
   DISPLAY ITEMS
--------------------------------------------------------- */

function displayItems(items) {

    if (currentCategory !== "all") {
        items = items.filter(
            item => item.category === currentCategory
        );
    }

    if (items.length === 0) {
        itemsContainer.innerHTML = `
            <div class="empty">
                No items found.
            </div>
        `;

        return;
    }

    itemsContainer.innerHTML = items.map(item => {

        const tags = (item.tags || [])
            .map(
                tag =>
                    `<span class="tag">#${escapeHtml(tag)}</span>`
            )
            .join("");

        return `
            <article class="item-card">

                <div class="item-top">

                    <h3 class="item-title">
                        ${escapeHtml(item.title)}
                    </h3>

                    <span class="category">
                        ${escapeHtml(item.category)}
                    </span>

                </div>

                <p class="item-content">
                    ${escapeHtml(item.content)}
                </p>

                <div class="tags">
                    ${tags}
                </div>

            </article>
        `;

    }).join("");
}


/* ---------------------------------------------------------
   SEARCH
--------------------------------------------------------- */

searchInput.addEventListener("input", () => {

    clearTimeout(searchTimeout);

    searchTimeout = setTimeout(
        performSearch,
        250
    );
});


async function performSearch() {

    const query = searchInput.value.trim();

    if (!query) {
        await loadItems();
        return;
    }

    try {

        let url =
            `${API_URL}/search?q=${encodeURIComponent(query)}`;

        if (currentCategory !== "all") {
            url +=
                `&category=${encodeURIComponent(currentCategory)}`;
        }

        const response = await fetch(url);

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Search failed");
        }

        const items = data.map(result => result[1]);

        displayItems(items);

    } catch (error) {

        console.error("Search error:", error);

        itemsContainer.innerHTML = `
            <div class="empty">
                Search failed.
            </div>
        `;
    }
}


/* ---------------------------------------------------------
   CATEGORY FILTERS
--------------------------------------------------------- */

filters.forEach(filter => {

    filter.addEventListener("click", () => {

        filters.forEach(
            button => button.classList.remove("active")
        );

        filter.classList.add("active");

        currentCategory =
            filter.dataset.category;

        if (searchInput.value.trim()) {
            performSearch();
        } else {
            loadItems();
        }

    });

});


/* ---------------------------------------------------------
   ADD ITEM MODAL
--------------------------------------------------------- */

addButton.addEventListener("click", () => {

    modal.classList.remove("hidden");

    titleInput.focus();

});


closeModal.addEventListener("click", () => {

    modal.classList.add("hidden");

});


modal.addEventListener("click", event => {

    if (event.target === modal) {
        modal.classList.add("hidden");
    }

});


/* ---------------------------------------------------------
   SAVE ITEM
--------------------------------------------------------- */

itemForm.addEventListener("submit", async event => {

    event.preventDefault();

    const tags = tagsInput.value
        .split(",")
        .map(tag => tag.trim())
        .filter(tag => tag.length > 0);


    const item = {

        title: titleInput.value.trim(),

        content: contentInput.value.trim(),

        category: categoryInput.value,

        tags: tags

    };


    if (!item.title || !item.content) {
        alert("Please enter a title and content.");
        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/items`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(item)
            }
        );


        const data = await response.json();


        if (!response.ok) {
            throw new Error(
                data.detail || "Failed to save item"
            );
        }


        console.log("Saved:", data);


        itemForm.reset();

        modal.classList.add("hidden");

        await loadItems();


    } catch (error) {

        console.error("Save error:", error);

        alert(
            `Could not save item.\n\n${error.message}`
        );

    }

});


/* ---------------------------------------------------------
   HTML ESCAPING
--------------------------------------------------------- */

function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");

}


/* ---------------------------------------------------------
   START
--------------------------------------------------------- */

loadItems();