function isObject(obj) {
    return typeof obj === 'object' && !!obj;
}

function getNowFormattedDate() {
    let today = new Date();
    let YYYY = today.getFullYear();
    let MM = correctNumNotation(today.getMonth()+1);
    let DD = correctNumNotation(today.getDate());
    let HH = correctNumNotation(today.getHours());
    let mm = correctNumNotation(today.getMinutes());
    let ss = correctNumNotation(today.getSeconds());

    return `${YYYY + MM + DD + '_' + HH + mm + ss}`;
}

function correctNumNotation(val) {
    return val<10 ? `0${val}` : val;
}

export {isObject};