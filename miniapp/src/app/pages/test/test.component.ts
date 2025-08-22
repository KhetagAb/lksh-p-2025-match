import { Component, OnInit } from '@angular/core';
import * as telegram from '@telegram-apps/sdk';
import * as models from '../../api/models';

@Component({
  selector: 'app-test',
  standalone: true,
  imports: [],
  templateUrl: './test.component.html',
  styleUrl: './test.component.scss'
})
export class TestComponent implements OnInit {

  details = "";

  ngOnInit(): void {
  }
}
