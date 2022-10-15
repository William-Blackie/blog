import hljs from 'highlight.js';
import '../css/main.css';
import Menu from './components/menu';

document.addEventListener('DOMContentLoaded', () => {

    if (document.querySelector(Menu.selector())) {
        new Menu();
    }
    hljs.highlightAll();
});