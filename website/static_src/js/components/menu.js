class Menu {
    constructor() {
        this.menuButton = document.querySelector('#menu-button');
        this.menu = document.querySelector('#menu');
        this.menuClose = document.querySelector('#menu-close');
        this.invisibleClass = 'hidden';
        this.bindEventListeners();
    }

    hideMenu() {
        if (!this.menu.classList.contains(this.invisibleClass)) {
            this.menu.classList.add(this.invisibleClass);
        }
    }

    showMenu() {
        if (this.menu.classList.contains(this.invisibleClass)) {
            this.menu.classList.remove(this.invisibleClass)
        }
    }
    toggleMenu() {
        if (this.menu.classList.contains(this.invisibleClass)) {
            this.showMenu()
        } else {
            this.hideMenu()
        }
    }


    bindEventListeners() {
        // Open / Close menu via menu button
        this.menuButton.addEventListener('click', (e) => {
            this.toggleMenu()
        });
        // Close menu 
        this.menuClose.addEventListener('click', (e) => {
            this.toggleMenu()
        });
        this.menu.querySelectorAll('a').forEach((element) => {
            element.addEventListener('click', (e) => {
                this.menu.classList.add(this.invisibleClass);
            })
        })
    }
}

export default Menu;