function sendData() {
    const data = { message: "Данные из Web App" };
    Telegram.WebApp.sendData(JSON.stringify(data));
}
