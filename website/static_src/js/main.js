import hljs from 'highlight.js';
import '../css/main.css';
import Menu from './components/menu';

document.addEventListener('DOMContentLoaded', () => {
    new Menu();
    hljs.highlightAll();
});