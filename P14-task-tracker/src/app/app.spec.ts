import { TestBed } from '@angular/core/testing';
import { App } from './app';
import { KaziService } from './kazi.service';

describe('App', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
    }).compileComponents();
  });

  it('huunda app', () => {
    const fixture = TestBed.createComponent(App);
    expect(fixture.componentInstance).toBeTruthy();
  });

  it('huonyesha kichwa', async () => {
    const fixture = TestBed.createComponent(App);
    await fixture.whenStable();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('Fuatilia Kazi');
  });

  it('kichujio cha awali = zote (kazi 3 zinaonekana)', async () => {
    const fixture = TestBed.createComponent(App);
    await fixture.whenStable();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelectorAll('.orodha li').length).toBe(3);
  });

  it('kubadilisha kichujio kunapunguza orodha', async () => {
    const fixture = TestBed.createComponent(App);
    await fixture.whenStable();
    const app = fixture.componentInstance as unknown as {
      wekaKichujio: (k: 'zote' | 'kamili' | 'haijamalizika') => void;
    };
    app.wekaKichujio('haijamalizika');
    await fixture.whenStable();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelectorAll('.orodha li').length).toBe(2);
    app.wekaKichujio('kamili');
    await fixture.whenStable();
    expect(
      fixture.nativeElement.querySelectorAll('.orodha li').length
    ).toBe(1);
  });
});

describe('KaziService', () => {
  let huduma: KaziService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    huduma = TestBed.inject(KaziService);
  });

  it('kuanzia: kazi 3, kamili 1', () => {
    expect(huduma.kazi().length).toBe(3);
    expect(huduma.kamili()).toBe(1);
    expect(huduma.haijamalizika()).toBe(2);
  });

  it('idhini inabadilisha hali', () => {
    huduma.idhini(2);
    expect(huduma.kamili()).toBe(2);
    huduma.idhini(2);
    expect(huduma.kamili()).toBe(1);
  });

  it('ongeza huongeza kazi mpya na hukata neno tupu', () => {
    huduma.ongeza('  Soma TypeScript  ');
    expect(huduma.kazi().length).toBe(4);
    expect(huduma.kazi()[3].jina).toBe('Soma TypeScript');
    huduma.ongeza('   ');
    expect(huduma.kazi().length).toBe(4);
  });
});
