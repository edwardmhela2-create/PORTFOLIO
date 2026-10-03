import { Component, computed, inject, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { KaziService, Kichujio } from './kazi.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly huduma = inject(KaziService);

  protected readonly title = signal('Fuatilia Kazi');
  protected readonly kichujio = signal<Kichujio>('zote');
  protected readonly jinaJipya = signal('');

  protected readonly zilizochujwa = computed(() => {
    const kichujio = this.kichujio();
    const zote = this.huduma.kazi();
    if (kichujio === 'kamili') {
      return zote.filter(k => k.imekamilika);
    }
    if (kichujio === 'haijamalizika') {
      return zote.filter(k => !k.imekamilika);
    }
    return zote;
  });

  protected wekaKichujio(k: Kichujio): void {
    this.kichujio.set(k);
  }

  protected wekaJina(tukio: Event): void {
    const tumbo = tukio.target as HTMLInputElement;
    this.jinaJipya.set(tumbo.value);
  }

  protected ongezaKazi(): void {
    this.huduma.ongeza(this.jinaJipya());
    this.jinaJipya.set('');
  }
}
