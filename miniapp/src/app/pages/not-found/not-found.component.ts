import { Component, Inject, OnInit, Optional } from '@angular/core';

@Component({
  selector: 'app-not-found-page',
  template: `
      <h1>Not Found</h1>
      <p>This page does not exist.</p>
  `,
  styles: `
      * {
        text-align: center;
      }
  `
})
export class NotFoundComponent {

  constructor() { }
}
