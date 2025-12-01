let currentIndex = 0;
let totalBooks = 0;
let booksData = []; // Store all books data
const historyStack = [];
let nextRandomIndex = -1;

const titleEl = document.getElementById('book-title');
const descEl = document.getElementById('book-description');
const coverEl = document.getElementById('book-cover');
const spinnerEl = document.getElementById('loading-spinner');
const issueNumEl = document.getElementById('issue-num');
const pageNumEl = document.getElementById('page-num');

// Load all books data at start
async function loadBooksData() {
    try {
        const response = await fetch('books.json');
        booksData = await response.json();
        totalBooks = booksData.length;
        console.log(`Loaded ${totalBooks} books.`);

        // Initial render after loading
        renderBook(0, false);
    } catch (error) {
        console.error("Error loading books data:", error);
        titleEl.textContent = "Error loading data";
        descEl.textContent = "Please try refreshing the page.";
    }
}

function getBookData(index) {
    if (booksData.length === 0) return null;
    // Ensure index wraps around
    const safeIndex = index % totalBooks;
    const book = booksData[safeIndex];
    return {
        ...book,
        index: safeIndex,
        total: totalBooks
    };
}

function getRandomIndex() {
    if (totalBooks === 0) return 0;
    return Math.floor(Math.random() * totalBooks);
}

async function renderBook(index, pushToHistory = true) {
    if (booksData.length === 0) return;

    // Show loading state for image
    coverEl.style.display = 'none';
    spinnerEl.style.display = 'flex';
    titleEl.textContent = "LOADING...";
    descEl.textContent = "Loading story...";

    const book = getBookData(index);
    if (!book) return;

    // Update History
    if (pushToHistory && currentIndex !== index) {
        historyStack.push(currentIndex);
    }

    // Update Basic Info
    currentIndex = book.index;

    titleEl.textContent = book.title;
    issueNumEl.textContent = currentIndex + 1;
    pageNumEl.textContent = Math.floor(Math.random() * 30) + 1; // Random page number for flavor

    // Handle Image
    coverEl.onload = () => {
        spinnerEl.style.display = 'none';
        coverEl.style.display = 'block';
    };
    coverEl.src = book.image_url;

    // If image is already cached/loaded by browser, onload might not fire
    if (coverEl.complete) {
        spinnerEl.style.display = 'none';
        coverEl.style.display = 'block';
    }

    // Display Explanation
    if (book.explanation) {
        descEl.textContent = book.explanation;
    } else {
        descEl.textContent = "Explanation not available.";
    }

    // Prepare Next Random Book
    nextRandomIndex = getRandomIndex();
    // Avoid immediate repeat if possible
    if (nextRandomIndex === currentIndex && totalBooks > 1) {
        nextRandomIndex = getRandomIndex();
    }

    console.log(`Current: ${currentIndex}, Next Random: ${nextRandomIndex}`);
}

document.getElementById('up-btn').addEventListener('click', () => {
    // Up is Previous (History)
    if (historyStack.length > 0) {
        const prevIndex = historyStack.pop();
        renderBook(prevIndex, false); // Don't push to history when going back
    } else {
        renderBook(getRandomIndex(), true);
    }
});

document.getElementById('down-btn').addEventListener('click', () => {
    // Down is Next (Random)
    if (nextRandomIndex !== -1) {
        renderBook(nextRandomIndex, true);
    } else {
        renderBook(getRandomIndex(), true);
    }
});

// Start by loading data
loadBooksData();
