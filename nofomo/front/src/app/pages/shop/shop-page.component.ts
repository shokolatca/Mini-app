import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-shop-page',
  templateUrl: './shop-page.component.html',
  styleUrls: ['./shop-page.component.scss']
})
export class ShopPageComponent {
  public shopForm: FormGroup;
  public totalPrice: number = 666; // Заглушка для цены

  constructor(private fb: FormBuilder) {
    //todo: убрать заглушку, отправлять фолрму через сервис
    this.shopForm = this.fb.group({
      accounts: [30], // Количество аккаунтов
      duration: [1], // Срок (месяцы)
      hasTelegramAccounts: [true] // Есть ли Telegram-аккаунты
    });
  }

  public makePayment(): void {
    console.log('Оплата совершена!', this.shopForm.value);
  }
}
