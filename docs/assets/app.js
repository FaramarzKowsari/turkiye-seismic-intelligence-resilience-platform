const buttons = document.querySelectorAll('.lang');
const translatable = document.querySelectorAll('[data-en][data-tr]');
buttons.forEach((button) => {
  button.addEventListener('click', () => {
    const language = button.dataset.lang;
    buttons.forEach((item) => item.classList.toggle('active', item === button));
    translatable.forEach((item) => { item.textContent = item.dataset[language]; });
    document.documentElement.lang = language;
  });
});
