let s = `tudelft-cyan??{cmyk}??{1,0,0,0}
tudelft-black??{cmyk}??{0,0,0,1}
tudelft-white??{cmyk}??{0,0,0,0}
tudelft-sea-green??{cmyk}??{0.54,0,0.32,0}
tudelft-green??{cmyk}??{1,0.15,0.4,0}
tudelft-dark-blue??{cmyk}??{1,0.66,0,0.4}
tudelft-purple??{cmyk}??{0.98,1,0,0.35}
tudelft-turquoise??{cmyk}??{0.82,0,0.21,0.08}
tudelft-sky-blue??{cmyk}??{0.45,0,0.06,0.06}
tudelft-lavender??{cmyk}??{0.45,0.2,0,0.07}
tudelft-orange??{cmyk}??{0.02,0.56,0.84,0}
tudelft-warm-purple??{cmyk}??{0.58,1,0,0.02}
tudelft-fuchsia??{cmyk}??{0.19,1,0,0.19}
tudelft-bright-green??{cmyk}??{0.36,0,1,0}
tudelft-yellow??{cmyk}??{0.02,0,0.54,0}`;

s = s.split('\n')

let colors = ``;
let pycode = ``;
s.forEach(line =>{
    line = line.split('??'); //[0] is name, [1] {cymk}, [2] is {c,y,m,k}
    let cymk = line[2].replace(/{|}/gi, '').split(',');
    let base = 255 * (1-cymk[3]);
    let r = Math.round(base * (1-cymk[0]));
    let g = Math.round(base * (1-cymk[1]));
    let b = Math.round(base * (1-cymk[2]));
    colors += `${line[0]}\t\t{rgb}\t{${r}, ${g}, ${b}}\n`;
    pycode += `${line[0]} = (${r}, ${g}, ${b})\n`;
});
console.log(pycode);