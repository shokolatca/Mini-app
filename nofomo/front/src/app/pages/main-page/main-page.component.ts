import { Component, ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MainPageComponent {
    //todo: связка с беком (загружать пользователя через сервис)
  public user = {
    userId: '#001488',
    username: 'RASH2409',
    referrals: 2,
    balance: 40,
  };

  public isEdit: boolean = false;

  toggleEdit() {
    this.isEdit = !this.isEdit;
  }

  invite() {
    alert('Invite link copied to clipboard!');
  }
}
