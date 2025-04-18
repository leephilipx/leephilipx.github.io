/*=============== CHANGE BACKGROUND HEADER ===============*/
function scrollHeader() {
    const header = document.getElementById('header')
    // When the scroll is greater than 50 viewport height, add the scroll-header class to the header tag
    if(this.scrollY >= 50) header.classList.add('scroll-header'); else header.classList.remove('scroll-header')
}
window.addEventListener('scroll', scrollHeader)


/*=============== WORK MODAL ===============*/
const modalViews = document.querySelectorAll('.work__modal'),
      modalBtns = document.querySelectorAll('.work__button'),
      modalCloses = document.querySelectorAll('.work__modal-close')

let modal = function(modalClick) {
    modalViews[modalClick].classList.add('active-modal')

}

modalBtns.forEach((mb, i) => {
    mb.addEventListener('click', () => { modal(i) })
})

modalCloses.forEach((mc) => {
    mc.addEventListener('click', () => {
        modalViews.forEach((mv) => {
            mv.classList.remove('active-modal')
        })
    })
})


/*=============== MIXITUP FILTER PORTFOLIO ===============*/
let mixerPorfolio = mixitup('.portfolio__container', {
    selectors: {
        target: '.portfolio__card'
    },
    animation: {
        duration: 300
    }
})

/* Link active work */ 
const linkWork = document.querySelectorAll('.portfolio__item')

function activeWork() {
    linkWork.forEach(l => l.classList.remove('active-portfolio'))
    this.classList.add('active-portfolio')
}

linkWork.forEach(l => l.addEventListener('click', activeWork))


/*=============== SWIPER TESTIMONIAL ===============*/
let swiperTestimonial = new Swiper('.testimonial__container', {
    spaceBetween: 24,
    loop: true,
    grabCursor: true,

    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    breakpoints: {
        576: {
            slidesPerView: 2,
        },
        768: {
            slidesPerView: 2,
            spaceBetween: 48,
        },
    }
})


/*=============== SCROLL SECTIONS ACTIVE LINK ===============*/
const sections = document.querySelectorAll('section[id]')

function scrollActive() {
    const scrollY = window.pageYOffset

    sections.forEach(current => {
        const sectionHeight = current.offsetHeight,
              sectionTop = current.offsetTop - 58,
              sectionId = current.getAttribute('id')

        if(scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            document.querySelector('.nav__menu a[href*=' + sectionId + ']').classList.add('active-link')
        } else {
            document.querySelector('.nav__menu a[href*=' + sectionId + ']').classList.remove('active-link')
        }
    })
}
window.addEventListener('scroll', scrollActive)


/*=============== LIGHT DARK THEME ===============*/ 
const themeButton = document.getElementById('theme-button')
const lightTheme = 'light-theme'
const iconTheme = 'bx-sun'

// Previously selected topic (if user selected)
const selectedTheme = localStorage.getItem('selected-theme')
const selectedIcon = localStorage.getItem('selected-icon')

// We obtain the current theme that the interface has by validating the dark-theme class
const getCurrentTheme = () => document.body.classList.contains(lightTheme) ? 'dark' : 'light'
const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'bx bx-moon' : 'bx bx-sun'

// We validate if the user previously chose a topic
if (selectedTheme) {
  // If the validation is fulfilled, we ask what the issue was to know if we activated or deactivated the light
  document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](lightTheme)
  themeButton.classList[selectedIcon === 'bx bx-moon' ? 'add' : 'remove'](iconTheme)
}

// Activate / deactivate the theme manually with the button
themeButton.addEventListener('click', () => {
    // Add or remove the dark / icon theme
    document.body.classList.toggle(lightTheme)
    themeButton.classList.toggle(iconTheme)
    // We save the theme and the current icon that the user chose
    localStorage.setItem('selected-theme', getCurrentTheme())
    localStorage.setItem('selected-icon', getCurrentIcon())
})


/*=============== SCROLL REVEAL ANIMATION ===============*/
const sr = ScrollReveal({
    origin: 'top',
    distance: '60px',
    duration: 2000,
    delay: 200,
    // reset: true,
})

sr.reveal(`.home__data`)
sr.reveal(`.home__handle`, {delay: 500})
sr.reveal(`.home__social, .home__scroll`, {delay: 700, duration: 3000, origin: 'bottom'})


/*=============== EMAIL CONTACT FORM ===============*/
emailjs.init('GdwABB-FTAn27989T');  // https://dashboard.emailjs.com/admin/account

window.onload = function() {
    document.getElementById('contact-form').addEventListener('submit', function(event) {

        event.preventDefault();

        // Client-side form validation
        if (document.getElementById('contact-form-name').value === '') {
            alert('Please enter your name!');
            return;
        } else if (document.getElementById('contact-form-email').value === '') {
            alert('Please enter your email address!');
            return;
        } else if (document.getElementById('contact-form-message').value === '') {
            alert('Please enter your message!');
            return;
        }

        // Send email
        emailjs.sendForm('service_bqopn9f', 'template_jnbv7vt', this)
            .then(function() {
                // console.log('EMAIL SUCCESS!');
                alert('Your message has been sent successfully!');
                document.getElementById('contact-form').reset();
            }, function(error) {
                // console.log('EMAIL FAILED ...', error);
                alert('Your message failed to send! Please check your Internet connection and try again.');
            });
    });
}


const navLogo = document.getElementById('navLogo');
const menu = document.getElementById('customMenu');

// Show custom menu
navLogo.addEventListener('contextmenu', function (e) {
  e.preventDefault(); // Prevent default right-click
  menu.style.top = `${e.pageY}px`;
  menu.style.left = `${e.pageX}px`;
  menu.style.display = 'block';
});

// Hide on click elsewhere
document.addEventListener('click', function () {
  menu.style.display = 'none';
});