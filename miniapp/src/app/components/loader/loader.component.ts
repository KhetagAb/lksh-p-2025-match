import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-loader',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './loader.component.html',
  styleUrl: './loader.component.scss'
})
export class LoaderComponent {
  @Input() size: 'small' | 'medium' | 'large' | 'custom' = 'medium';
  @Input() customSize?: string; 
  @Input() color?: string; 
  @Input() showPulse: boolean = true; 
  @Input() strokeWidth: number = 3;

  get loaderSize(): string {
    if (this.size === 'custom' && this.customSize) {
      return this.customSize;
    }
    
    const sizes = {
      small: '3rem',
      medium: '5rem',
      large: '8rem',
      custom: '5rem' 
    };
    
    return sizes[this.size];
  }

  get loaderColor(): string {
    return this.color || 'var(--tg-theme-button-color, #007aff)';
  }
}
