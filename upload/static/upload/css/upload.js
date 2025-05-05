document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('fileInput');
    const browseBtn = document.getElementById('browseBtn');
    const filesList = document.getElementById('filesList');
    const selectedFiles = document.getElementById('selectedFiles');
    const uploadBtn = document.getElementById('uploadBtn');
    const colorItems = document.querySelectorAll('.color-item');
    
    // Variables
    let files = [];
    let selectedColor = null;
    
    // Event Listeners
    browseBtn.addEventListener('click', () => fileInput.click());
    
    fileInput.addEventListener('change', handleFileSelect);
    
    dropArea.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropArea.classList.add('drag-over');
    });
    
    dropArea.addEventListener('dragleave', () => {
      dropArea.classList.remove('drag-over');
    });
    
    dropArea.addEventListener('drop', (e) => {
      e.preventDefault();
      dropArea.classList.remove('drag-over');
      
      if (e.dataTransfer.files.length) {
        handleFiles(e.dataTransfer.files);
      }
    });
    
    uploadBtn.addEventListener('click', uploadFiles);
    
    colorItems.forEach(item => {
      item.addEventListener('click', () => {
        // Remove selected class from all items
        colorItems.forEach(i => i.classList.remove('selected'));
        
        // Add selected class to clicked item
        item.classList.add('selected');
        
        // Store selected color
        selectedColor = {
          color: item.dataset.color,
          name: item.dataset.name
        };
        
        // Enable upload button if files are selected
        updateUploadButton();
      });
    });
    
    // Functions
    function handleFileSelect(e) {
      handleFiles(e.target.files);
    }
    
    function handleFiles(fileList) {
      // Convert FileList to Array and filter out files larger than 10MB
      const newFiles = Array.from(fileList).filter(file => {
        if (file.size > 10 * 1024 * 1024) {
          showToast('File too large', `${file.name} exceeds the 10MB limit.`, 'error');
          return false;
        }
        return true;
      });
      
      // Add new files to the files array
      files = [...files, ...newFiles];
      
      // Show selected files section
      if (files.length > 0) {
        selectedFiles.style.display = 'block';
      }
      
      // Render files list
      renderFilesList();
      
      // Update upload button state
      updateUploadButton();
    }
    
    function renderFilesList() {
      filesList.innerHTML = '';
      
      files.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        
        const fileExt = file.name.split('.').pop().toUpperCase();
        
        fileItem.innerHTML = `
          <div class="file-details">
            <div class="file-icon">${fileExt}</div>
            <div>
              <div class="file-name" title="${file.name}">${file.name}</div>
              <div class="file-size">${formatFileSize(file.size)}</div>
              <div class="progress-container" style="display: none;">
                <div class="progress-bar"></div>
              </div>
            </div>
          </div>
          <div class="file-actions">
            <button class="remove-file" data-index="${index}">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 6h18"></path>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"></path>
                <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
            </button>
          </div>
        `;
        
        filesList.appendChild(fileItem);
      });
      
      // Add event listeners to remove buttons
      document.querySelectorAll('.remove-file').forEach(button => {
        button.addEventListener('click', () => {
          const index = parseInt(button.dataset.index);
          files.splice(index, 1);
          renderFilesList();
          
          if (files.length === 0) {
            selectedFiles.style.display = 'none';
          }
          
          updateUploadButton();
        });
      });
    }
    
    function formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    function updateUploadButton() {
      uploadBtn.disabled = !(files.length > 0 && selectedColor);
    }
    
    function uploadFiles() {
      if (files.length === 0 || !selectedColor) {
        showToast('Error', 'Please select files and a color category.', 'error');
        return;
      }
      
      // Show progress for each file
      const progressBars = document.querySelectorAll('.progress-container');
      progressBars.forEach(container => {
        container.style.display = 'block';
      });
      
      // Simulate upload progress
      let progress = 0;
      const interval = setInterval(() => {
        progress += 5;
        
        document.querySelectorAll('.progress-bar').forEach(bar => {
          bar.style.width = `${progress}%`;
        });
        
        if (progress >= 100) {
          clearInterval(interval);
          
          // Simulate server response
          setTimeout(() => {
            showToast('Success', `${files.length} files uploaded to ${selectedColor.name} category.`, 'success');
            
            // Reset form
            files = [];
            selectedFiles.style.display = 'none';
            filesList.innerHTML = '';
            colorItems.forEach(item => item.classList.remove('selected'));
            selectedColor = null;
            updateUploadButton();
          }, 500);
        }
      }, 100);
    }
    
    function showToast(title, message, type = 'success') {
      // Remove existing toast
      const existingToast = document.querySelector('.toast');
      if (existingToast) {
        existingToast.remove();
      }
      
      // Create new toast
      const toast = document.createElement('div');
      toast.className = `toast toast-${type}`;
      
      toast.innerHTML = `
        <div class="toast-icon">
          ${type === 'success' 
            ? '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>'
            : '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>'
          }
        </div>
        <div class="toast-content">
          <div class="toast-title">${title}</div>
          <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      `;
      
      document.body.appendChild(toast);
      
      // Show toast
      setTimeout(() => {
        toast.classList.add('show');
      }, 10);
      
      // Add close event
      toast.querySelector('.toast-close').addEventListener('click', () => {
        toast.classList.remove('show');
        setTimeout(() => {
          toast.remove();
        }, 300);
      });
      
      // Auto hide after 5 seconds
      setTimeout(() => {
        if (document.body.contains(toast)) {
          toast.classList.remove('show');
          setTimeout(() => {
            if (document.body.contains(toast)) {
              toast.remove();
            }
          }, 300);
        }
      }, 5000);
    }
  });