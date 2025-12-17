const form = document.getElementById("giftForm")
const giftsContainer = document.getElementById("gifts");

async function markComplete(giftId, isChecked) {
    if (isChecked) {
        const response = await fetch(`/gifts/complete/${giftId}`, {
            method: 'POST',
    });
    await loadGifts()
    }
}

async function loadGifts() {
    const response = await fetch('/gifts');
    const gifts = await response.json(); 
    
    giftsContainer.innerHTML = '';
    
    gifts.sort((a, b) => a.complete - b.complete); 

    gifts.forEach(gift => {
        const item = document.createElement("div");
        item.classList.add('gift-item'); 
        
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.id = `gift-${gift.id}`;
        checkbox.checked = gift.complete === 1; 

        checkbox.addEventListener('change', (event) => {

            if (event.target.checked) {
                markComplete(gift.id, true);
            } else {
                alert("To uncomplete a gift, refresh the page and ensure you haven't clicked the box again.");
            }
        });

        const text = document.createElement("label");
        text.htmlFor = `gift-${gift.id}`; 
        
        if (gift.complete === 1) {
            text.innerHTML = `<del>Gift for ${gift.name}: ${gift.gift}</del>`;
        } else {
            text.textContent = `Gift for ${gift.name}: ${gift.gift}`;
        }
        
        // Append elements
        item.appendChild(checkbox);
        item.appendChild(text);
        giftsContainer.appendChild(item);
    });
}
form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const name = form.elements.name.value;
    const gift = form.elements.gift.value;

    await fetch('/gifts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, gift })
    });

    form.reset();
    await loadGifts(); 
});

loadGifts();