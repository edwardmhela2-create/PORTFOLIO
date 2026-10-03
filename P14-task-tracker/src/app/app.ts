import { Component, computed, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

export interface Kazi {
  id: number;
  jina: string;
  imekamilika: boolean;
}

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('Fuatilia Kazi');

  protected readonly kazi = signal<Kazi[]>([
    { id: 1, jina: 'Soma somo la Angular', imekamilika: true },
    { id: 2, jina: 'Andika component ya kwanza', imekamilika: false },
    { id: 3, jina: 'Endesha `ng serve`', imekamilika: false },
  ]);

  protected readonly kamiliZilizo = computed(
    () => this.kazi().filter(k => k.imekamilika).length
  );

  protected badiliza(id: number): void {
    this.kazi.update(list =>
      list.map(k => (k.id === id ? { ...k, imekamilika: !k.imekamilika } : k))
    );
  }
}
