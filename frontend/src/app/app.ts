import { Component, signal } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { ScuderiaComponent } from './scuderia/scuderia';


@Component({
  selector: 'app-root',
  imports: [RouterOutlet, ScuderiaComponent, RouterLink, RouterLinkActive],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}