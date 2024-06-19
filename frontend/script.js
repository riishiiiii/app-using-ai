async function registerUser() {
  const username = document.getElementById("register-username").value;
  const password = document.getElementById("register-password").value;
  console.log(username, password);
  const response = await fetch("http://0.0.0.0:8000/users/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });
  const data = await response.json();
  document.getElementById("register-message").style.display = "block";
  setTimeout(() => {
    document.getElementById("register-message").style.display = "none";
  }, 3000);
  if (response.ok) {
    document.getElementById("register-message").textContent = data.message;
    document
      .getElementById("register-message")
      .classList.remove("text-red-500");
    document
      .getElementById("register-message")
      .classList.add("text-green-500");
  } else {
    document.getElementById("register-message").textContent =
      data.message || "Error registering user";
    document
      .getElementById("register-message")
      .classList.remove("text-green-500");
    document
      .getElementById("register-message")
      .classList.add("text-red-500");
  }
}

async function loginUser() {
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;
  const response = await fetch("http://0.0.0.0:8000/users/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });
  const data = await response.json();
  document.getElementById("login-message").style.display = "block";
  setTimeout(() => {
    document.getElementById("login-message").style.display = "none";
  }, 3000);
  if (response.ok) {
    document.getElementById("login-message").textContent = data.message;
    document
      .getElementById("login-message")
      .classList.remove("text-red-500");
    document
      .getElementById("login-message")
      .classList.add("text-green-500");
    localStorage.setItem("access_token", data.access_token); // Store access token
    window.location.href = "blogs.html"; // Redirect to blogs page after successful login
  } else {
    document.getElementById("login-message").textContent =  
      data.message || "Error logging in";
    document
      .getElementById("login-message")
      .classList.remove("text-green-500");
    document
      .getElementById("login-message")
      .classList.add("text-red-500");
  }
}

async function writeBlog() {
  const title = document.getElementById("blog-title").value;
  const content = document.getElementById("blog-content").value;
  const token = localStorage.getItem("access_token"); // Get access token
  const response = await fetch("http://0.0.0.0:8000/blog/write_blog", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}` // Include access token in headers
    },
    body: JSON.stringify({ title, content }),
  });
  const data = await response.json();
  if (response.ok) {
    loadBlogs(); // Reload blogs after successful submission
  } else {
    console.error(data.message || "Error writing blog");
  }
}

async function loadBlogs() {
  const token = localStorage.getItem("access_token"); // Get access token
  const response = await fetch("http://0.0.0.0:8000/blog/get_blogs", {
    headers: {
      "Authorization": `Bearer ${token}` // Include access token in headers
    }
  });
  const blogs = await response.json();
  const blogsContainer = document.getElementById("blogs-container");
  blogsContainer.innerHTML = "";
  blogs.forEach((blog, index) => {
    const blogElement = document.createElement("div");
    blogElement.classList.add("p-4", "bg-white", "rounded", "shadow");
    blogElement.innerHTML = `
      <h2 class="text-2xl font-semibold mb-4 text-gray-800">${blog.title}</h2>
      <p class="text-gray-600 mb-4">${blog.content}</p>
      <div class="flex justify-end">
        <button class="delete-blog bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded transition duration-300 ease-in-out" data-id="${index}">Delete</button>
      </div>
    `;
    blogElement.addEventListener("click", () => {
      window.location.href = `blog.html?id=${blog.id}`;
    });
    blogElement.querySelector(".delete-blog").addEventListener("click", async (event) => {
      event.stopPropagation();
      const deleteResponse = await fetch(`http://0.0.0.0:8000/blog/delete_blog/${index}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}` // Include access token in headers
        }
      });
      if (deleteResponse.ok) {
        loadBlogs(); // Reload blogs after successful deletion
      } else {
        console.error("Error deleting blog");
      }
    });
    blogsContainer.appendChild(blogElement);
  });
}

// Load blogs when the page loads
document.addEventListener("DOMContentLoaded", loadBlogs);

function logoutUser() {
  localStorage.removeItem("access_token");
  window.location.href = "index.html"; // Redirect to home page after logout
}
