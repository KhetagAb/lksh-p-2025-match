import { Component, input } from '@angular/core';
import { RouterLink, Router } from '@angular/router';
import { MenuButton } from '../../services/menu.service';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './menu.component.html',
  styleUrl: './menu.component.scss'
})
export class MenuComponent {
  buttons = input<MenuButton[]>([]);

  constructor(private router: Router) {}

  isActive(buttonId: string): boolean {
    return this.router.url === `/${buttonId}` || this.router.url.startsWith(`/${buttonId}`);
  }
}
