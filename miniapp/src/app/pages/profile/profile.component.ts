import { Component, inject, OnInit } from '@angular/core';
import { TelegramService } from '../../services/telegram.service';
import { PlayersService } from '../../api/services';
import { Player } from '../../api/models';
import { CommonModule } from '@angular/common';
import { LoaderComponent } from '../../components/loader/loader.component';
import { Router } from '@angular/router';
import * as tg from '@telegram-apps/sdk';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, LoaderComponent],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.scss'
})
export class ProfileComponent implements OnInit {

  telegram = inject(TelegramService);
  user: any = null;
  player: Player | null = null;
  isServerError = false;
  isImageLoading = true;
  imageLoadError = false;

  constructor(
	private playersService: PlayersService,
	private router: Router,
  ) {}

  ngOnInit(): void {
    this.user = this.telegram.getUser();
    var apiRequestData = { tg_id: this.user.id };

    this.playersService.corePlayerByTgGet(apiRequestData).subscribe({
      next: (response) => {
        this.player = response.player;
        var strJsonResponse = JSON.stringify(this.player);
        console.log("[Pages:General] Got answer: ", strJsonResponse);
      },
      error: (error) => {
        console.error("[Pages:General] Got error: ", error);
        setTimeout(() => {
          this.isServerError = true;
        }, 200);
      }
    });
  }

  onImageLoad() {
    setTimeout(() => {
      this.isImageLoading = false;
    }, 50);
  }

  onImageError() {
    this.isImageLoading = false;
    this.imageLoadError = true;
  }
}
