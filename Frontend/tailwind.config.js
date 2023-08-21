/** @type {import('tailwindcss').Config} */
module.exports = {
   content: [
     "./src/**/*.{js,jsx,ts,tsx}",
   ],
   theme: {
    fontSize: {
      sm: '0.8rem',
      base: '1rem',
      xl: '1.25rem',
      '2xl': '1.563rem',
      '2x' : '1.746rem',
      '3xl': '1.953rem',
      '4xl': '2.441rem',
      '5xl': '3.052rem',
    },
    
     extend: {
      padding: {
        '100' : '500px',
        'popup' : '550px',
        'popup2' : '500px',
        'popup3' : '480px',
        'h' : '7px',
        'k' : '113px',  
      },
      gridTemplateRows: {
        '[auto,auto,1fr]': 'auto auto 1fr',
     },
     height: {
      'page': '145vh',
    },
    },
   },
   plugins: [
    require('@tailwindcss/aspect-ratio'),
   ],
 }