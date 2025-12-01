let currentIndex = 0;
let totalBooks = 0;
const cache = {}; // Stores { index: { data: bookData, explanation: string } }
const historyStack = [];
let nextRandomIndex = -1;

const titleEl = document.getElementById('book-title');
const descEl = document.getElementById('book-description');
const coverEl = document.getElementById('book-cover');
const spinnerEl = document.getElementById('loading-spinner');
const issueNumEl = document.getElementById('issue-num');
const pageNumEl = document.getElementById('page-num');

async function fetchBookData(index) {
    if (cache[index] && cache[index].data) {
        return cache[index].data;
    }
    try {
        const response = await fetch(`/api/book/${index}`);
        const data = await response.json();
        if (!cache[index]) cache[index] = {};
        cache[index].data = data;
        return data;
    } catch (error) {
        console.error("Error fetching book:", error);
        return null;
    }
}

async function fetchExplanation(index, originalTitle, title, stockStatus, pagePerCost) {
    if (cache[index] && cache[index].explanation) {
        return cache[index].explanation;
    }
    try {
        const params = new URLSearchParams();
        if (originalTitle) params.append('original_title', originalTitle);
        if (title) params.append('title', title);
        if (stockStatus) params.append('stock_status', stockStatus);
        if (pagePerCost) params.append('page_per_cost', pagePerCost);

        const response = await fetch(`/api/explain?${params.toString()}`);
        const data = await response.json();

        if (!cache[index]) cache[index] = {};
        cache[index].explanation = data.description;
        return data.description;
    } catch (error) {
        console.error("Error fetching explanation:", error);
        return "설명을 불러오는 중 오류가 발생했습니다.";
    }
}

function getRandomIndex() {
    if (totalBooks === 0) return 0;
    return Math.floor(Math.random() * totalBooks);
}

async function renderBook(index, pushToHistory = true) {
    // Show loading state for image if not cached
    if (!cache[index] || !cache[index].data) {
        coverEl.style.display = 'none';
        spinnerEl.style.display = 'flex';
        titleEl.textContent = "LOADING...";
        descEl.textContent = "Loading story...";
    }

    const book = await fetchBookData(index);
    if (!book) return;

    // Update History
    if (pushToHistory && currentIndex !== index) {
        historyStack.push(currentIndex);
    }

    // Update Basic Info
    currentIndex = book.index;
    totalBooks = book.total;

    titleEl.textContent = book.title;
    issueNumEl.textContent = currentIndex + 1;
    pageNumEl.textContent = Math.floor(Math.random() * 30) + 1; // Random page number for flavor

    // Handle Image
    coverEl.onload = () => {
        spinnerEl.style.display = 'none';
        coverEl.style.display = 'block';
    };
    coverEl.src = book.image_url;

    // If image is already cached/loaded by browser, onload might not fire, so check complete
    if (coverEl.complete) {
        spinnerEl.style.display = 'none';
        coverEl.style.display = 'block';
    }

    // Fetch and Display Explanation
    descEl.textContent = "AI가 이야기를 읽고 있습니다...";
    const explanation = await fetchExplanation(currentIndex, book.original_title, book.title, book.stock_status, book.page_per_cost);
    descEl.textContent = explanation;

    // Prepare Next Random Book
    nextRandomIndex = getRandomIndex();
    // Avoid immediate repeat if possible
    if (nextRandomIndex === currentIndex && totalBooks > 1) {
        nextRandomIndex = getRandomIndex();
    }

    console.log(`Current: ${currentIndex}, Next Random: ${nextRandomIndex}`);
    prefetch(nextRandomIndex);
}

function prefetch(index) {
    fetchBookData(index).then(book => {
        if (book) {
            fetchExplanation(book.index, book.original_title, book.title, book.stock_status, book.page_per_cost);
        }
    });
}

document.getElementById('up-btn').addEventListener('click', () => {
    // Up is Previous (History)
    if (historyStack.length > 0) {
        const prevIndex = historyStack.pop();
        renderBook(prevIndex, false); // Don't push to history when going back
    } else {
        // If no history, just go to another random one? Or stay?
        // Let's go to a random one to keep it moving.
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

// Initial Load: Random start
// We need to fetch at least one book to know 'totalBooks' for true random.
// But we can start with a guess or just 0, then the first fetch updates totalBooks.
// Let's start with 0, then jump to random? Or just fetch 0.
// Better: Fetch 0 to get count, then render random?
// Or just render 0.
renderBook(0, false).then(() => {
    // After first load, we know totalBooks.
    // If we want the *very first* book to be random, we could do:
    // renderBook(Math.floor(Math.random() * totalBooks));
    // But 0 is fine for start.
});
