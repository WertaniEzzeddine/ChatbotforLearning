import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../services/auth.service';
import { CourseService } from '../services/course.service';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-learning-chat-bot',
  templateUrl: './learning-chat-bot.component.html',
  styleUrls: ['./learning-chat-bot.component.scss']
})
export class LearningChatBotComponent {
  Summarize:boolean=true;
  isToggled:boolean=false;
  chatMessages: { course_id: number, sender: string; text: string }[] = [];
   userMessage: string = '';
  
  name: string = '';
  userId: number = 0;
  file: File | null = null;
  currentCourse:any;
  showNewCourseForm = false;
  queryText: string = '';
  botResponse: string | null = null;
  courses: any; // Example course list
  
  constructor(private courseService: CourseService,private authService: AuthService, private http: HttpClient) {}
  sendMessage() {
    if (this.queryText.trim()) {
       this.chatMessages.push({course_id:this.currentCourse.id, sender: 'user', text: this.queryText });
       this.botReply(this.queryText);
       this.queryText = '';
    }
 }

 botReply(userInput: string) {
  this.courseService
  .sendMessage(this.currentCourse.id, 'user', this.queryText)
  .subscribe((response) => {
    this.chatMessages.push({course_id:this.currentCourse.id, sender: 'bot', text: response.text });
    
  });
   }

  toggleNewCourseForm() {
    this.showNewCourseForm = !this.showNewCourseForm;
  }

  onFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input && input.files && input.files[0]) {
      this.file = input.files[0];
    }
  }

  handleFormSubmission() {
    this.userId=this.authService.user.id
    if (this.name && this.userId && this.file) {
      this.courseService.uploadCourse(this.name, this.userId, this.file).subscribe(
        (response) => {
          console.log('Course uploaded successfully', response);
          this.currentCourse=response.course
          this.showNewCourseForm=false;
          this.courses.push(this.currentCourse);
          
        },
        (error) => {
          console.error('Upload failed', error);
          alert('Failed to upload course.');
        }
      );
    } else {
      alert('Please fill all fields and select a file.');
    }
   
  }

  submitQuery() {
   
  }

  startLearning() {
    console.log('Learning started');
    // Implement your learning process here
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
  }

  onFileDrop(event: DragEvent) {
    event.preventDefault();
    const files = event.dataTransfer?.files;
    if (files && files[0]) {
      this.file = files[0];
    }
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input && input.files && input.files[0]) {
      this.file = input.files[0];
    }
  }


  loadChatHistory(course:any) {
    this.currentCourse=course
    this.courseService.getChatHistory(this.currentCourse.id).subscribe((history) => {
      this.chatMessages = history;
    });
  }

  

  ngOnInit(): void {
    
      this.courseService.getCoursesByUser().subscribe(
        (response) => {
          this.courses = response.courses;
          console.log('Courses:', this.courses);
        },
        (error) => {
          console.error('Error fetching courses:', error);
        }
      );
    
  }

}
