import { Injectable } from '@angular/core';

export interface MenuButton {
  id: string;
  text: string;
  icon: string;
}

export const menuButtons: MenuButton[] = [
  {
    id: "profile",
    text: "Профиль",
    icon: "👤",
  },
  {
    id: "general",
    text: "Главная",
    icon: "⭐",
  },
  {
    id: "support",
    text: "Поддержка",
    icon: "❓",
  },
];

@Injectable({
  providedIn: 'root'
})
export class MenuService {

  constructor() { }
}
