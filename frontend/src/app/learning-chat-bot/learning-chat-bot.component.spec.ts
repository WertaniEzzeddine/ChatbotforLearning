import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LearningChatBotComponent } from './learning-chat-bot.component';

describe('LearningChatBotComponent', () => {
  let component: LearningChatBotComponent;
  let fixture: ComponentFixture<LearningChatBotComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LearningChatBotComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LearningChatBotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
