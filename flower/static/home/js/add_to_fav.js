document.addEventListener("DOMContentLoaded", function () {
    const favoriteButtons = document.querySelectorAll(".favorite-btn");
    favoriteButtons.forEach((button) => {
        button.addEventListener("click", function (e) {
            e.preventDefault();
            const productId = this.getAttribute("data-product-id");
            const icon = this.querySelector("i");
            
            // Получаем CSRF токен из cookie
            // Получаем CSRF токен из meta-тега
            const csrftoken = document.querySelector('meta[name="csrf-token"]').content;
            
            fetch(`/favorites/toggle-favorite/${productId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify({}) // Пустое тело, так как нам нужен только заголовок
            })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === "added") {
                    icon.classList.remove("far");
                    icon.classList.add("fas");
                    icon.style.color = "red";
                } else if (data.status === "removed") {
                    icon.classList.remove("fas");
                    icon.classList.add("far");
                    icon.style.color = "#ccc";
                }
            })
            .catch((error) => console.error("Error:", error));
        });
    });
});
