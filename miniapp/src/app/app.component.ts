import { Component, OnInit, OnDestroy, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { TelegramService } from './services/telegram.service';
import { MenuComponent } from './components/menu/menu.component';
import { menuButtons } from './services/menu.service';
import * as tg from '@telegram-apps/sdk';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, MenuComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'Match';

  telegramSrv = inject(TelegramService);

  menuButtons = menuButtons;

  private cleanupFunctions: (() => void)[] = [];
  private intervalIds: number[] = [];

  constructor(
	private route: ActivatedRoute,
	private router: Router,
  ) {
  }

  async ngOnInit(): Promise<void> {
    try {
      await this.telegramSrv.initializeSDK();
      await this.telegramSrv.setupComponents();
      this.telegramSrv.setupMiniApp()

    } catch (error) {
      console.error('Failed to initialize Telegram Mini App:', error);
    }
  }

  ngOnDestroy(): void {
    this.intervalIds.forEach(id => clearInterval(id));
    this.cleanupFunctions.forEach(cleanup => cleanup());

    this.telegramSrv.cleanup();
  }

  mainButtonHandler = (): void => {
    this.telegramSrv.triggerHapticFeedback('medium');
  }
}
