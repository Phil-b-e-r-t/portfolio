/* ==========================================
   AMPURIRA PHILBERT PORTFOLIO
   JAVASCRIPT FILE
========================================== */

// ================= TYPING EFFECT =================
const typingText = document.querySelector(".typing");


const words = [
    "Software Engineer",    "Web Developer",
    "Python Programmer",
    "Database Designer",
    "Problem Solver"
];

let wordIndex = 0;
let charIndex = 0;
let deleting = false;

function typeEffect(){

    let currentWord = words[wordIndex];

    if(!deleting){

        typingText.textContent =
        currentWord.substring(0,charIndex++);

        if(charIndex > currentWord.length){

            deleting = true;

            setTimeout(typeEffect,1500);

            return;

        }

    }else{

        typingText.textContent =
        currentWord.substring(0,charIndex--);

        if(charIndex < 0){

            deleting=false;

            wordIndex++;

            if(wordIndex >= words.length){

                wordIndex=0;

            }

        }

    }

    setTimeout(typeEffect,100);

}

typeEffect();

// ================= MOBILE MENU =================
const menuBtn =
document.querySelector(".menu-btn");

const navLinks =
document.querySelector(".nav-links");

menuBtn.addEventListener("click",()=>{

    navLinks.classList.toggle("active");

});

// Close menu after clicking link
document.querySelectorAll(".nav-links a")
.forEach(link=>{

    link.addEventListener("click",()=>{

        navLinks.classList.remove("active");
    });

});

// ================= DARK / LIGHT MODE =================
const themeBtn =
document.querySelector(".theme-btn");

let lightMode=false;

themeBtn.addEventListener("click",()=>{

    lightMode=!lightMode;

    if(lightMode){

        document.documentElement.style.setProperty(
            "--bg",
            "#f8fafc"
        );

        document.documentElement.style.setProperty(
            "--card",
            "#e2e8f0"
        );

        document.documentElement.style.setProperty(
            "--text",
            "#0f172a"
        );

        document.documentElement.style.setProperty(
            "--muted",
            "#475569"
        );

        themeBtn.classList.replace(
            "fa-moon",
            "fa-sun"
        );

    }
    else{

        document.documentElement.style.setProperty(
            "--bg",
            "#0f172a"
        );
        document.documentElement.style.setProperty(
            "--card",
            "#1e293b"
        );

        document.documentElement.style.setProperty(
            "--text",
            "#f8fafc"
        );

        document.documentElement.style.setProperty(
            "--muted",
            "#cbd5e1"
        );

        themeBtn.classList.replace(
            "fa-sun",
            "fa-moon"
        );

    }

});

// ================= SCROLL REVEAL =================

const hiddenElements =
document.querySelectorAll(
".skill-box, .service-card, .project-card, .timeline-item"
);

const observer =
new IntersectionObserver((entries)=>{

entries.forEach(entry=>{

    if(entry.isIntersecting){

        entry.target.classList.add("show");

    }

});

});

hiddenElements.forEach(element=>{
    element.classList.add("hidden");
    observer.observe(element);
});

// ================= COUNTER ANIMATION =================
const counters =
document.querySelectorAll(".counter");
counters.forEach(counter=>{

    let target =
    Number(counter.textContent);

    let count=0;

    let interval =
    setInterval(()=>{
        count++;
        counter.textContent=count;

        if(count>=target){
            clearInterval(interval);
        }

    },100);

});

// ================= SCROLL TO TOP =================
const scrollBtn =
document.getElementById("scrollTop");

window.addEventListener("scroll",()=>{

    if(window.scrollY > 500){
        scrollBtn.style.display="block";

    }
    else{
        scrollBtn.style.display="none";
    }

});

scrollBtn.addEventListener("click",()=>{
    window.scrollTo({

        top:0,
        behavior:"smooth"

    });

});

// ================= CONTACT FORM =================
