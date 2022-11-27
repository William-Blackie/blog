module.exports = {
    content: [
        './website/templates/**/*.{html,js}',
        './website/utils/constants.py',
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
}