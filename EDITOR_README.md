# Website Template Editor

A comprehensive Python-based visual editor for website templates with real-time preview capabilities. This tool allows complete customization of your website template including content, design, images, and layout.

## Features

### 🎨 **Visual Design Control**
- **Color Customization**: Change all website colors with color picker
- **Logo Management**: Upload, resize, and position custom logos
- **Typography Control**: Modify fonts and text styles
- **Custom CSS**: Add your own CSS for advanced styling

### 📝 **Content Management**
- **Text Editing**: Edit all website text content
- **Section Management**: Add, remove, reorder content sections
- **Meta Information**: Control SEO title, description, and metadata
- **Navigation**: Customize menu items and branding

### 🖼️ **Image Management**
- **Upload Images**: Add new images to your website
- **Resize & Position**: Control image dimensions and positioning
- **Frame Styles**: Apply different frames (rounded, circle, shadow, border)
- **Responsive Images**: Automatic mobile and desktop optimization

### 🔧 **Tile System**
- **Add Tiles**: Create custom content tiles
- **Image Tiles**: Add pictures to tiles with custom frames
- **Resizable**: Make tiles any size you want
- **Movable**: Drag and drop tiles to reposition
- **Link Support**: Add links to tiles for navigation

### 📱 **Responsive Design**
- **Mobile Optimized**: All changes maintain mobile compatibility
- **Desktop Layout**: Optimized for desktop viewing
- **Cross-Device**: Consistent appearance across all devices

### 🔄 **Real-Time Preview**
- **Live Server**: Built-in HTTP server for immediate preview
- **Instant Updates**: See changes immediately as you make them
- **Browser Integration**: Open preview in your default browser

### 📦 **Version Control**
- **Automatic Versioning**: Each export gets a unique version number
- **Timestamp**: All exports include creation timestamp
- **File Management**: Original template preserved, new versions created

## Installation

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)
- Pillow (PIL) for image processing

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Editor
```bash
python website_editor.py
```

## Usage Guide

### 1. **Loading Your Template**
1. Launch the editor
2. Go to **File > Load Template** or use the Template tab
3. Select your website template folder
4. The editor will analyze your template structure

### 2. **Content Editing**
1. Switch to the **Content** tab
2. Edit meta information (title, description)
3. Modify navigation and branding
4. Add/edit content sections

### 3. **Design Customization**
1. Go to the **Design** tab
2. Use color pickers to change website colors
3. Upload and configure your logo
4. Add custom CSS for advanced styling

### 4. **Image Management**
1. Use the **Images** tab
2. Add new images with "Add Image"
3. Select images to edit properties
4. Set dimensions, frames, and positioning

### 5. **Tile Management**
1. Switch to the **Tiles** tab
2. Create new tiles with "Add Tile"
3. Add images, text, and links to tiles
4. Choose different tile styles

### 6. **Preview & Export**
1. Go to **Preview & Export** tab
2. Click "Start Preview Server"
3. Click "Open in Browser" to see live preview
4. Set version name and click "Export Website"

## Configuration Options

### **Meta Information**
- Website title
- SEO description
- Author information
- Keywords

### **Design Elements**
- Primary color scheme
- Secondary colors
- Accent colors
- Background colors
- Text colors

### **Logo Settings**
- Logo file (SVG, PNG, JPG supported)
- Width and height
- Alt text
- Positioning

### **Image Properties**
- Dimensions (width/height)
- Frame styles:
  - None
  - Rounded corners
  - Circle
  - Drop shadow
  - Border
- Positioning:
  - Left aligned
  - Center aligned
  - Right aligned
  - Float left
  - Float right

### **Tile Styles**
- Default
- Featured
- Minimal
- Card style
- Overlay style

## File Structure

The editor works with the following template structure:
```
template_folder/
├── index.html          # Main HTML file
├── styles/
│   └── main.css       # Main stylesheet
├── fix.css            # Override styles
├── scripts/
│   └── main.js        # JavaScript files
├── images/            # Image assets
└── custom_styles.css  # Generated custom styles
```

## Export Features

### **Version Control**
- Each export creates a new folder with version and timestamp
- Format: `v1.1_20250910_143022`
- Original template is never modified

### **Included Files**
- All template files with modifications
- Custom CSS with your changes
- Configuration JSON file
- All uploaded images

### **Generated Files**
- `custom_styles.css`: Your custom styling
- `website_config.json`: Complete configuration backup

## Advanced Features

### **Responsive Design**
All changes automatically include responsive breakpoints:
- Desktop (1200px+)
- Tablet (768px-1199px)
- Mobile (767px and below)

### **CSS Integration**
The editor generates clean, modern CSS:
```css
:root {
    --primary-color: #007AFF;
    --secondary-color: #5856D6;
    /* Your custom colors */
}
```

### **Image Optimization**
- Automatic image resizing for web
- Format optimization
- Responsive image handling

## Troubleshooting

### **Preview Server Issues**
- Make sure port 8090 is available
- Check firewall settings
- Try restarting the preview server

### **Image Upload Problems**
- Ensure images directory exists
- Check file permissions
- Supported formats: JPG, PNG, SVG, GIF, WebP

### **Export Errors**
- Verify write permissions in template directory
- Ensure enough disk space
- Check template file integrity

## Tips for Best Results

1. **Start with Template**: Always load your template first
2. **Backup Original**: Keep a backup of your original template
3. **Test Responsiveness**: Always check mobile preview
4. **Use Web-Safe Fonts**: Stick to standard web fonts
5. **Optimize Images**: Resize images before upload for better performance
6. **Regular Exports**: Export versions regularly as backups

## Support

For issues or feature requests:
1. Check the export log for error messages
2. Verify all dependencies are installed
3. Ensure Python version compatibility
4. Check file permissions in template directory

## Version History

- **v1.0**: Initial release with full editing capabilities
- Real-time preview system
- Complete responsive design support
- Advanced image and tile management

## License

This tool is designed specifically for the Hamid Haghmoradi website template but can be adapted for other templates with similar structure.
