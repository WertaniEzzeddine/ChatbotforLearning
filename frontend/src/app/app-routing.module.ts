import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { NavbarComponent } from './navbar/navbar.component';
import { LoginComponent } from './login/login.component';
import { SingupComponent } from './singup/singup.component';
import { LearningChatBotComponent } from './learning-chat-bot/learning-chat-bot.component';
import { HomeComponent } from './home/home.component';
import { AuthGuard } from './auth.guard';
const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'nav', component: NavbarComponent },
  { path: 'login', component: LoginComponent },
  { path: 'signup', component: SingupComponent   },
  { path: 'chat', component: LearningChatBotComponent  , canActivate: [AuthGuard] }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
