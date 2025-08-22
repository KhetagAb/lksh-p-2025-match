import { Injectable } from '@angular/core';
import { postEvent } from '@telegram-apps/bridge';
import * as tg from '@telegram-apps/sdk'

@Injectable({
  providedIn: 'root'
})
export class TelegramService {

  isInitialized = false;
  userInfo: any = null;

  private cleanupFunctions: (() => void)[] = [];
  private intervalIds: number[] = [];

  constructor() { }

  async initializeSDK(): Promise<void> {
    try {
      tg.init();
      this.isInitialized = true;

      if (typeof tg.initData.restore === 'function') {
        tg.initData.restore();
        const user = tg.initData.user();
        if (user) {
          this.userInfo = user;
        }
      }

      console.log('Telegram SDK initialized successfully');
    } catch (error) {
      console.error('Telegram SDK initialization error:', error);
      throw error;
    }
  }

  getUser(): any {
    if (typeof tg.initData.restore === 'function') {
      tg.initData.restore();
      const user = tg.initData.user();
      if (user) {
        return user;
      }
    }
  }

  async setupComponents(): Promise<void> {
    await this.mountComponents();
    const launchParams = tg.retrieveLaunchParams();
    console.log(launchParams);

    if (tg.viewport.isMounted() && tg.viewport.requestFullscreen.isAvailable() && this.isMobile()) {
      await tg.viewport.requestFullscreen();
    }
  }

  isMobile(): boolean {
    const launchParams = tg.retrieveLaunchParams();
    return ['android', 'ios'].includes(launchParams.tgWebAppPlatform ?? '');
  }

  cleanup(): void {
    this.intervalIds.forEach(id => clearInterval(id));
    this.cleanupFunctions.forEach(cleanup => cleanup());

    this.unmountComponents();
  }

  async mountComponents(): Promise<void> {
    try {
      if (tg.miniApp.mount.isAvailable()) {
        console.log('[TelegramService] tg.miniApp: mounting');
        await tg.miniApp.mount();
      } else {
        console.log('[TelegramService] tg.miniApp.mount not available');
      }

      if (tg.viewport.mount.isAvailable()) {
        console.log('[TelegramService] tg.viewport: mounting');
        await tg.viewport.mount();

        if (tg.viewport.bindCssVars.isAvailable()) {
          console.log('[TelegramService] tg.viewport: bindCssVars');
          tg.viewport.bindCssVars();
        }

        if (tg.viewport.expand.isAvailable()) {
          tg.viewport.expand();
        }
        try { console.log('[TelegramService] tg.viewport size', tg.viewport.width(), tg.viewport.height()); } catch(e) {}
      } else {
        console.log('[TelegramService] tg.viewport.mount not available');
      }

      if (tg.themeParams.mount.isAvailable()) {
        console.log('[TelegramService] tg.themeParams: mounting');
        await tg.themeParams.mount();

        if (tg.themeParams.bindCssVars.isAvailable()) {
          console.log('[TelegramService] tg.themeParams: bindCssVars');
          tg.themeParams.bindCssVars();
        } else {
          console.log('[TelegramService] tg.themeParams.bindCssVars not available');
        }
      } else {
        console.log('[TelegramService] tg.themeParams.mount not available');
      }

      if (tg.backButton.mount.isAvailable()) tg.backButton.mount();
      if (tg.mainButton.mount.isAvailable()) tg.mainButton.mount();
      if (tg.secondaryButton.mount.isAvailable()) tg.secondaryButton.mount();
      if (tg.swipeBehavior.mount.isAvailable()) {
        tg.swipeBehavior.mount();
        if (tg.swipeBehavior.disableVertical.isAvailable()) tg.swipeBehavior.disableVertical();
      }
    } catch (err) {
      console.warn('[TelegramService] mountComponents error', err);
    }
  }

  setupMiniApp(): void {
    try {
      if (tg.themeParams.isMounted()) {
        tg.themeParams.unmount();
      }

      if (tg.miniApp?.ready?.isAvailable() ?? false) {
        console.log('[TelegramService] tg.miniApp: ready()');
        tg.miniApp.ready();
      } else if (typeof tg.miniApp?.ready === 'function') {
        try { tg.miniApp.ready(); } catch(e) {}
      } else {
        console.log('[TelegramService] tg.miniApp.ready not available');
      }

      var style = window.getComputedStyle(document.body);
      var secondaryBgColor = style.getPropertyValue('--tg-theme-secondary-bg-color');
      if (tg.miniApp?.setBackgroundColor?.isAvailable() ?? false) {
        console.log('[TelegramService] tg.miniApp.setBackgroundColor: applying ', secondaryBgColor);
        tg.miniApp.setBackgroundColor(secondaryBgColor);
      } else {
        console.log('[TelegramService] tg.miniApp.setBackgroundColor not available — applying fallback to document.body');
        try { document.body.style.backgroundColor = secondaryBgColor; } catch(e) {}
      }

      if (tg.themeParams.mount.isAvailable() && !tg.themeParams.isMounted()) {
        tg.themeParams.mount();
        if (tg.themeParams.bindCssVars.isAvailable()) {
          tg.themeParams.bindCssVars();
        }
      }

    } catch (err) {
      console.warn('[TelegramService] setupMiniApp error', err);
    }
  }


  unmountComponents(): void {
    if (tg.backButton.isMounted()) {
      tg.backButton.unmount();
    }
    if (tg.mainButton.isMounted()) {
      tg.mainButton.unmount();
    }
    if (tg.secondaryButton.isMounted()) {
      tg.secondaryButton.unmount();
    }
    if (tg.viewport.isMounted()) {
      tg.viewport.unmount();
    }
    if (tg.themeParams.isMounted()) {
      tg.themeParams.unmount();
    }
    if (tg.swipeBehavior.isMounted()) {
      tg.swipeBehavior.unmount();
    }
    if (tg.miniApp.isMounted()) {
      tg.miniApp.unmount();
    }
  }

  public triggerHapticFeedback(
    type: 'light' | 'medium' | 'heavy' | 'success' | 'warning' | 'error'
  ): void {
    switch (type) {
      case 'light':
      case 'medium':
      case 'heavy':
        if (tg.hapticFeedback.impactOccurred.isAvailable()) {
          tg.hapticFeedback.impactOccurred(type);
        }
        break;
      case 'success':
      case 'warning':
      case 'error':
        if (tg.hapticFeedback.notificationOccurred.isAvailable()) {
          tg.hapticFeedback.notificationOccurred(type);
        }
        break;
    }
  }
}
