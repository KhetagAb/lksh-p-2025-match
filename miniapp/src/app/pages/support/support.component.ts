import { CommonModule } from '@angular/common';
import { LoaderComponent } from '../../components/loader/loader.component';
import * as tg from '@telegram-apps/sdk';
import { Router } from '@angular/router';
import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'app-support',
  standalone: true,
  imports: [CommonModule, LoaderComponent],
  templateUrl: './support.component.html',
  styleUrl: './support.component.scss',
  encapsulation: ViewEncapsulation.None
})
export class SupportComponent {
  mail = "support@match.lksh.ru (не работает)";
  isImageLoading = true;
  imageError = false;

  constructor(
  ) {}

  onCopyMailButtonClick() {
	var button = document.querySelector('#copy-button');
	navigator.clipboard.writeText(this.mail);
  }
}
