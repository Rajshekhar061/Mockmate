import os
import json
import logging
from django.utils import timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.conf import settings

from .models import Resume
from .forms import ResumeUploadForm
from .utils.pdf_extractor import extract_text_from_pdf, is_searchable_pdf
from ai_engine.services.groq_service import GroqService

logger = logging.getLogger(__name__)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def upload_resume(request):
    """
    Handle resume upload and initiate AI analysis.
    """
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Create resume record
                resume = form.save(commit=False)
                resume.user = request.user
                resume.original_filename = request.FILES['uploaded_file'].name
                resume.status = 'processing'
                resume.save()
                
                # Get file path
                file_path = resume.uploaded_file.path
                
                # Extract text from PDF
                success, extracted_text, error = extract_text_from_pdf(file_path)
                
                if not success:
                    resume.status = 'failed'
                    resume.error_message = error or "Failed to extract text from PDF"
                    resume.save()
                    messages.error(
                        request,
                        f"Failed to process resume: {error}"
                    )
                    return redirect('dashboard')
                
                # Check if PDF is searchable
                if not is_searchable_pdf(file_path):
                    resume.status = 'failed'
                    resume.error_message = "Resume appears to be image-based. Please upload a text-based PDF."
                    resume.save()
                    messages.error(
                        request,
                        "Your resume appears to be scanned as an image. Please upload a text-based PDF for analysis."
                    )
                    return redirect('dashboard')
                
                # Store extracted text
                resume.extracted_text = extracted_text
                resume.save()
                
                # Analyze resume with Groq AI
                try:
                    groq = GroqService()
                    analysis_result = groq.analyze_resume(extracted_text)
                    
                    if 'error' not in analysis_result:
                        # Update resume with analysis results
                        resume.ats_score = analysis_result.get('ats_score', 0)
                        resume.strengths = analysis_result.get('strengths', [])
                        resume.weaknesses = analysis_result.get('weaknesses', [])
                        resume.suggestions = analysis_result.get('suggestions', [])
                        resume.keywords_found = analysis_result.get('keywords_analysis', {}).get('keywords_found', [])
                        resume.analysis_details = analysis_result
                        resume.status = 'completed'
                        resume.analyzed_at = timezone.now()
                        resume.save()
                        
                        messages.success(
                            request,
                            f"Resume analyzed successfully! ATS Score: {resume.ats_score}%"
                        )
                    else:
                        # Analysis failed but extraction succeeded
                        resume.status = 'failed'
                        resume.error_message = analysis_result.get('error', 'Unknown error during analysis')
                        resume.save()
                        messages.error(
                            request,
                            "Failed to analyze resume. Please try again later."
                        )
                        
                except Exception as e:
                    logger.error(f"Groq API error: {str(e)}")
                    resume.status = 'failed'
                    resume.error_message = f"API Error: {str(e)}"
                    resume.save()
                    messages.error(
                        request,
                        "AI service temporarily unavailable. Please try again later."
                    )
                
                return redirect('resume_feedback', resume_id=resume.id)
                
            except Exception as e:
                logger.error(f"Error uploading resume: {str(e)}")
                messages.error(
                    request,
                    f"An error occurred while processing your resume: {str(e)}"
                )
                return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ResumeUploadForm()
    
    context = {
        'form': form,
        'page_title': 'Upload Resume',
    }
    return render(request, 'resumes/upload_resume.html', context)


@login_required(login_url='login')
@require_http_methods(["GET"])
def resume_feedback(request, resume_id):
    """
    Display resume analysis feedback.
    """
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if not resume.is_analyzed():
        if resume.status == 'failed':
            messages.error(request, f"Resume analysis failed: {resume.error_message}")
        else:
            messages.info(request, "Resume is still being analyzed. Please check back in a moment.")
    
    context = {
        'resume': resume,
        'page_title': 'Resume Feedback',
        'strengths': resume.get_strengths_list(),
        'weaknesses': resume.get_weaknesses_list(),
        'suggestions': resume.get_suggestions_list(),
    }
    return render(request, 'resumes/resume_feedback.html', context)


@login_required(login_url='login')
@require_http_methods(["GET"])
def resume_list(request):
    """
    Display list of user's resumes.
    """
    resumes = Resume.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'resumes': resumes,
        'page_title': 'My Resumes',
    }
    return render(request, 'resumes/resume_list.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def delete_resume(request, resume_id):
    """
    Delete a resume.
    """
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    filename = resume.original_filename or resume.uploaded_file.name
    
    try:
        # Delete the file
        if resume.uploaded_file:
            if os.path.exists(resume.uploaded_file.path):
                os.remove(resume.uploaded_file.path)
        
        # Delete the database record
        resume.delete()
        messages.success(request, f"Resume '{filename}' deleted successfully.")
    except Exception as e:
        logger.error(f"Error deleting resume: {str(e)}")
        messages.error(request, "Failed to delete resume. Please try again.")
    
    return redirect('resume_list')


@login_required(login_url='login')
@require_http_methods(["GET"])
def reanalyze_resume(request, resume_id):
    """
    Reanalyze a previously uploaded resume.
    """
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if not resume.extracted_text:
        messages.error(request, "Cannot reanalyze resume without extracted text.")
        return redirect('resume_feedback', resume_id=resume.id)
    
    try:
        resume.status = 'processing'
        resume.save()
        
        # Reanalyze with Groq
        groq = GroqService()
        analysis_result = groq.analyze_resume(resume.extracted_text)
        
        if 'error' not in analysis_result:
            resume.ats_score = analysis_result.get('ats_score', 0)
            resume.strengths = analysis_result.get('strengths', [])
            resume.weaknesses = analysis_result.get('weaknesses', [])
            resume.suggestions = analysis_result.get('suggestions', [])
            resume.keywords_found = analysis_result.get('keywords_analysis', {}).get('keywords_found', [])
            resume.analysis_details = analysis_result
            resume.status = 'completed'
            resume.analyzed_at = datetime.utcnow()
            resume.save()
            
            messages.success(request, f"Resume reanalyzed! New ATS Score: {resume.ats_score}%")
        else:
            resume.status = 'failed'
            resume.error_message = analysis_result.get('error', 'Unknown error')
            resume.save()
            messages.error(request, "Failed to reanalyze resume.")
            
    except Exception as e:
        logger.error(f"Error reanalyzing resume: {str(e)}")
        resume.status = 'failed'
        resume.error_message = str(e)
        resume.save()
        messages.error(request, "An error occurred during reanalysis.")
    
    return redirect('resume_feedback', resume_id=resume.id)
