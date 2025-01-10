//declare global {
    //interface Window {
        //Telegram: any;
    //}
//}

const tg = window.Telegram.WebApp;

tg.expand();

function sendData() {
    const data = { message: "Данные из Web App" };
    tg.sendData(JSON.stringify(data));
}

const button = document.createElement("button");
button.innerText = "Отправить данные боту";
button.onclick = sendData;
document.body.appendChild(button);
