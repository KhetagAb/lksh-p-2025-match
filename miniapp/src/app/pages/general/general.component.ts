import { Component, OnInit, OnDestroy } from '@angular/core';
import * as tg from '@telegram-apps/sdk'
import { SportSectionsService } from '../../api/services';
import { SportSectionList } from '../../api/models';

@Component({
  selector: 'app-general',
  imports: [],
  templateUrl: './general.component.html',
  styleUrl: './general.component.scss'
})
export class GeneralComponent implements OnInit {
  sportSectionList: SportSectionList | null = null;
  details = "Loading..";
  serverError: string | null = null;

  constructor(private sportSectionsService: SportSectionsService) {}

  ngOnInit(): void {
    console.log("[Pages:General] Creating request to server");
    
	this.sportSectionsService.coreSportListGet().subscribe({
      next: (response) => {
        this.sportSectionList = response.sports_sections;
        var strJsonResponse = JSON.stringify(this.sportSectionList);
        console.log("[Pages:General] Got answer: ", strJsonResponse);
      },
      error: (error) => {
        console.error("[Pages:General] Got error: ", error);
        this.serverError = error.error;
        this.details = "Received Error";
      }
    });


  }
}
