import { Routes } from '@angular/router';
import { TestComponent } from './pages/test/test.component';
import { SportComponent } from './pages/sport/sport.component';
import { ActivityComponent } from './pages/activity/activity.component';
import { SupportComponent } from './pages/support/support.component';
import { GeneralComponent } from './pages/general/general.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { NotFoundComponent } from "./pages/not-found/not-found.component";

export const routes: Routes = [
  { path: 'test', component: TestComponent },
  { path: '', redirectTo: 'test', pathMatch: 'full' },
  { path: 'profile', component: ProfileComponent },
  { path: 'general', component: GeneralComponent },
  { path: 'support', component: SupportComponent },
  { path: 'sport/:id', component: SportComponent },
  { path: 'activity/:id', component: ActivityComponent },
  { path: '**', component: NotFoundComponent }
];
