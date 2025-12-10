# Media Player Requirements Document

## 1. Project Overview

### 1.1 Project Name
Cross-Platform Python Media Player

### 1.2 Project Description
A fully-featured, cross-platform media player application built with Python, targeting macOS and Windows platforms. The application will provide VLC-equivalent functionality with a modern, intuitive GUI.

### 1.3 Project Goals
- Create a robust, performant media player comparable to VLC
- Support comprehensive media format compatibility
- Ensure seamless cross-platform operation (macOS & Windows)
- Provide an intuitive, user-friendly interface
- Maintain clean, maintainable, and extensible codebase

---

## 2. Technical Requirements

### 2.1 Architecture & Design

#### 2.1.1 System Architecture
- **Multi-layered Architecture**:
  - Presentation Layer (GUI)
  - Business Logic Layer (Playback Engine, Media Processing)
  - Data Access Layer (File I/O, Network Streaming)
  - Platform Abstraction Layer (OS-specific APIs)

- **Component Architecture**:
  - **Core Engine**: Playback control, media decoding, synchronization
  - **GUI Module**: User interface, event handling, visual feedback
  - **Media Handler**: Format detection, codec management, metadata extraction
  - **Audio Subsystem**: Audio processing, output routing, effects
  - **Video Subsystem**: Video rendering, scaling, effects, hardware acceleration
  - **Subtitle Engine**: Parsing, rendering, synchronization
  - **Playlist Manager**: Queue management, persistence, ordering
  - **Configuration Manager**: Settings storage, platform-specific configs
  - **Network Module**: Streaming protocols, caching, buffering

#### 2.1.2 Design Patterns
- **MVC Pattern**: Separate Model (media data), View (GUI), Controller (logic)
- **Observer Pattern**: GUI updates based on playback state changes
- **Strategy Pattern**: Different decoding/rendering strategies based on capabilities
- **Factory Pattern**: Create appropriate decoders/renderers based on file type
- **Command Pattern**: Undo/redo for playlist operations, action history
- **Singleton Pattern**: Application configuration manager, logging system
- **State Pattern**: Playback states (playing, paused, stopped, buffering, error)
- **Facade Pattern**: Simplify complex subsystem interactions
- **Adapter Pattern**: Platform-specific API abstraction

#### 2.1.3 SOLID Principles Adherence
- **Single Responsibility**: Each class has one well-defined purpose
- **Open/Closed**: Plugin architecture for extensibility without modification
- **Liskov Substitution**: Interchangeable implementations (decoders, renderers)
- **Interface Segregation**: Specific interfaces (IMediaDecoder, IVideoRenderer, IAudioOutput, ISubtitleProvider, IPlaylistManager)
- **Dependency Inversion**: Depend on abstractions with dependency injection

#### 2.1.4 Modularity & Structure
- Package structure:
  ```
  simple-media-player/
  ├── src/
  │   ├── core/           # Core playback engine
  │   │   ├── player.py
  │   │   ├── decoder.py
  │   │   └── synchronizer.py
  │   ├── gui/            # GUI components
  │   │   ├── main_window.py
  │   │   ├── controls.py
  │   │   ├── dialogs.py
  │   │   └── widgets.py
  │   ├── media/          # Media handling
  │   │   ├── formats.py
  │   │   ├── metadata.py
  │   │   └── codecs.py
  │   ├── audio/          # Audio subsystem
  │   │   ├── engine.py
  │   │   ├── effects.py
  │   │   └── output.py
  │   ├── video/          # Video subsystem
  │   │   ├── renderer.py
  │   │   ├── filters.py
  │   │   └── acceleration.py
  │   ├── subtitles/      # Subtitle engine
  │   │   ├── parser.py
  │   │   └── renderer.py
  │   ├── playlist/       # Playlist management
  │   │   └── manager.py
  │   ├── network/        # Streaming & network
  │   │   ├── streaming.py
  │   │   └── protocols.py
  │   ├── utils/          # Utility functions
  │   │   ├── logging.py
  │   │   └── helpers.py
  │   ├── platform/       # Platform-specific code
  │   │   ├── macos.py
  │   │   └── windows.py
  │   ├── plugins/        # Plugin system
  │   └── config/         # Configuration management
  ├── tests/              # Unit and integration tests
  ├── resources/          # Icons, themes, etc.
  └── docs/               # Documentation
  ```

### 2.2 Technology Stack

#### 2.2.1 Core Technologies
- **Programming Language**: Python 3.10+
- **GUI Framework**: PyQt6 / PySide6
- **Media Backend**: libmpv (python-mpv) or libvlc (python-vlc)
- **Media Processing**: FFmpeg / PyAV

#### 2.2.2 Platform-Specific Technologies
- **macOS**:
  - VideoToolbox (hardware decoding)
  - Metal (GPU rendering)
  - Core Audio (audio output)
  - AVFoundation (media framework)
  
- **Windows**:
  - DirectX Video Acceleration (DXVA)
  - Direct3D 11 (GPU rendering)
  - WASAPI (audio output)
  - Media Foundation (media framework)

#### 2.2.3 Supporting Libraries
- Audio/Video: av, sounddevice, numpy
- File handling: pathlib, send2trash, watchdog
- Network: requests, aiohttp, yt-dlp
- Metadata: mutagen, pymediainfo
- Subtitles: pysrt, pysubs2
- Configuration: pyyaml, python-dotenv, platformdirs
- Testing: pytest, pytest-qt, pytest-cov
- Code quality: black, flake8, mypy
- Build tools: PyInstaller, py2app, cx_Freeze

### 2.3 Performance Requirements

#### 2.3.1 Playback Performance
- **Frame Rate**: Maintain consistent 60 FPS for video playback up to 4K resolution
- **Latency**: Audio-video sync must be within ±50ms
- **Startup Time**: Application launch < 2 seconds
- **File Loading**: Media file loading < 1 second for files up to 2GB
- **Seeking**: Frame-accurate seeking with < 500ms response time
- **Memory Usage**: 
  - Base application: < 100MB RAM
  - During playback: < 500MB RAM for 1080p, < 1GB for 4K
  - Efficient memory cleanup after file close

#### 2.3.2 Resource Management
- **CPU Utilization**: 
  - < 10% CPU for audio playback
  - < 30% CPU for 1080p video playback
  - Hardware acceleration when available
- **GPU Acceleration**: 
  - Utilize Metal (macOS) and DirectX/OpenGL (Windows)
  - Fallback to software decoding if hardware unavailable
- **Disk I/O**: 
  - Efficient buffering strategy (2-5 second buffer)
  - Minimize disk thrashing during playback
- **Network Streaming**: 
  - Adaptive bitrate streaming support
  - Pre-buffering for smooth playback

#### 2.3.3 Optimization Techniques
- Multi-threaded architecture:
  - Separate thread for GUI (main thread)
  - Separate thread for audio decoding
  - Separate thread for video decoding
  - Separate thread for file I/O
- Lazy loading of non-essential features
- Frame dropping algorithm for performance degradation
- Smart caching for recently accessed media
- Memory pooling for frame buffers

### 2.4 Code Quality Standards

#### 2.4.1 Code Standards
- PEP 8 compliance for all Python code
- Type hints for all function signatures
- Comprehensive docstrings (Google or NumPy style)
- Maximum function complexity: Cyclomatic complexity < 10
- Maximum file length: 500 lines
- Minimum test coverage: 80%

#### 2.4.2 Error Handling
- Graceful degradation for unsupported formats
- Comprehensive exception handling with user-friendly messages
- Logging system with multiple levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Crash recovery mechanism (save state before crashes)
- Detailed error reporting for debugging

#### 2.4.3 Testing Strategy
- Unit tests for all core components (>80% coverage)
- Integration tests for playback pipeline
- Performance benchmarks and profiling
- UI automated testing
- Cross-platform testing (CI/CD)
- Memory leak detection
- Stress testing with large files and long sessions

---

## 3. Functional Requirements

### 3.1 UX Design & Visual Identity

#### 3.1.0 Design Philosophy
**Core Principles:**
- **Modern & Minimalist**: Clean interface with purposeful use of color
- **Professional Yet Vibrant**: Balance between corporate polish and engaging visuals
- **Intuitive Navigation**: Zero learning curve for basic functions
- **CEO-Ready**: Premium look suitable for executive demonstrations
- **Responsive Design**: Smooth animations and visual feedback

**Color Philosophy:**
- Primary colors convey professionalism with strategic pops of vibrant accent colors
- Dark mode prioritizes eye comfort with rich, saturated accent colors
- Light mode uses softer pastels with deeper accent colors for contrast
- Color coding for different media types and states

#### 3.1.0.1 Visual Design Language

**Color Palette:**

*Light Mode (Default Professional)*
- **Background**: Clean white (#FFFFFF) with subtle grey gradients (#F8F9FA)
- **Primary Accent**: Modern blue (#2563EB) - buttons, active elements
- **Secondary Accent**: Vibrant purple (#8B5CF6) - highlights, special features
- **Success/Playing**: Energetic green (#10B981) - play indicators
- **Warning**: Warm amber (#F59E0B) - buffering, notifications
- **Error**: Professional red (#EF4444) - errors, stop button
- **Text Primary**: Deep grey (#1F2937)
- **Text Secondary**: Medium grey (#6B7280)
- **Borders/Dividers**: Light grey (#E5E7EB)

*Dark Mode (Premium Experience)*
- **Background**: Rich dark (#1A1B1E) with charcoal undertones (#2D2E32)
- **Primary Accent**: Electric blue (#3B82F6) - vibrant against dark
- **Secondary Accent**: Neon purple (#A78BFA) - premium feel
- **Success/Playing**: Bright green (#34D399) - high visibility
- **Warning**: Bright amber (#FCD34D) - clear indicators
- **Error**: Bright red (#F87171) - attention grabbing
- **Text Primary**: Pure white (#FFFFFF)
- **Text Secondary**: Light grey (#D1D5DB)
- **Borders/Dividers**: Subtle grey (#374151)

**Typography:**
- **Headings**: SF Pro Display (macOS) / Segoe UI (Windows) - Bold 18-24px
- **Body**: SF Pro Text (macOS) / Segoe UI (Windows) - Regular 14px
- **Monospace/Time**: SF Mono (macOS) / Consolas (Windows) - 12-14px
- **Line height**: 1.5 for readability
- **Letter spacing**: -0.01em for modern feel

**Spacing & Layout:**
- **Golden Ratio**: 8px base unit (8, 16, 24, 32, 48, 64px)
- **Breathing Room**: Generous padding for touchscreen compatibility
- **Card-based Design**: Subtle elevation shadows for depth
- **Rounded Corners**: 8px radius for modern, friendly appearance

**Icons & Imagery:**
- **Icon Style**: Duotone icons with gradient fills
- **Icon Size**: 24px standard, 32px for primary actions, 16px for secondary
- **Illustration Style**: Flat design with subtle shadows and gradients
- **Loading States**: Smooth skeleton screens with shimmer effect

#### 3.1.0.2 Textual UI Sketch - Main Window

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ≡  PyMedia Player                                    ⊡  ▭  ✕          │ ← Title bar (gradient: #2563EB → #8B5CF6)
├─────────────────────────────────────────────────────────────────────────┤
│ File  Playback  Audio  Video  Subtitle  Tools  View  Help              │ ← Menu bar (white text, semi-transparent overlay)
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │                                                                 │    │
│  │                    [VIDEO DISPLAY AREA]                        │    │
│  │                                                                 │    │
│  │              ╔═══════════════════════════╗                     │    │
│  │              ║  🎬 Drop media here       ║  ← Centered with   │    │
│  │              ║     or click to browse     ║     gradient icon  │    │
│  │              ║                            ║     (when no video)│    │
│  │              ║  Supported: MP4, MKV, AVI ║                     │    │
│  │              ╚═══════════════════════════╝                     │    │
│  │                                                                 │    │
│  │          [When playing: Full video with smooth scaling]        │    │
│  │                                                                 │    │
│  │  ┌─ OVERLAY CONTROLS (fade in on hover, auto-hide) ─────┐     │    │
│  │  │  ▶  ⏸  ⏹  ⏮  ⏭   [████████████░░░░░░] 2:35/4:20     │     │    │
│  │  │  🔊 ━━━━━●━━━━ 75%   [⚙]  [⛶]                       │     │    │
│  │  └────────────────────────────────────────────────────────┘    │    │
│  └───────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─ CONTROL PANEL (Fixed bottom, gradient background) ───────────┐    │
│  │                                                                 │    │
│  │  ▶/⏸   [━━━━━━━━━━━━━━━━━━━━━●━━━━━━━━━━━━━━] 2:35/4:20    │    │
│  │  Play   ├─ Vibrant gradient progress (blue→purple) ─┤    Time│    │
│  │         └─ Hover: Thumbnail preview popup ──┘                  │    │
│  │                                                                 │    │
│  │  ⏹  ⏮  ⏭  🔊━━●━ 75%  [🔄]  [🔀]  [⚡1.0x]  [CC]  [⛶]  [☰]  │    │
│  │  Stop Prev Next Volume  Loop Shuffle Speed  Subs Full  List   │    │
│  │                                                                 │    │
│  │  ┌─ STATUS BAR (subtle, informative) ─────────────────────┐   │    │
│  │  │ 🟢 Playing • H.264 1080p 60fps • AAC Stereo • 45.2 MB  │   │    │
│  │  └────────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘

COLOR NOTES:
- Title bar: Gradient from electric blue to vibrant purple
- Video area: Deep black (#000000) with subtle 1px border
- Control panel: Semi-transparent frosted glass effect
- Progress bar: Gradient fill (blue → purple) with glow effect
- Buttons: Circular with subtle shadows, hover = scale 1.1
- Active elements: Pulsing glow animation
- Volume slider: Gradient matching brand colors
```

#### 3.1.0.3 Textual UI Sketch - Playlist Sidebar

```
┌────────────────────────────────────────┐
│  PLAYLIST              [+] [⋯] [✕]    │ ← Header with gradient
├────────────────────────────────────────┤
│  🔍 Search playlist...                 │ ← Rounded search box
├────────────────────────────────────────┤
│  📂 Now Playing              [4 items] │
│  ┌──────────────────────────────────┐ │
│  │ ▶ Summer_Vacation.mp4      4:32  │ │ ← Playing (green accent)
│  │   └─ Progress: ███████░░░ 75%   │ │
│  └──────────────────────────────────┘ │
│  ┌──────────────────────────────────┐ │
│  │ 2 Tutorial_Video.mkv      12:45  │ │ ← Queue (grey)
│  │   └─ H.264 • 1080p               │ │
│  └──────────────────────────────────┘ │
│  ┌──────────────────────────────────┐ │
│  │ 3 Documentary.mp4         45:20  │ │
│  │   └─ HEVC • 4K                   │ │
│  └──────────────────────────────────┘ │
│  ┌──────────────────────────────────┐ │
│  │ 4 Music_Concert.avi       32:10  │ │
│  │   └─ AVI • 720p                  │ │
│  └──────────────────────────────────┘ │
│                                        │
│  [Drag & drop reordering enabled]     │
│  [Right-click for context menu]       │
├────────────────────────────────────────┤
│  ⟳ Repeat: Off  |  🔀 Shuffle: On    │ ← Playback modes
└────────────────────────────────────────┘

COLOR NOTES:
- Header: Subtle gradient background
- Playing item: Green left border (4px), light green tint
- Hover: Smooth scale (1.02) with shadow
- Drag indicator: Vibrant purple dashed outline
- Search box: White with blue focus ring
```

#### 3.1.0.4 Textual UI Sketch - Settings/Preferences Window

```
┌───────────────────────────────────────────────────────────────────┐
│  ⚙ Preferences                                        [✕]         │
├───────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌─ SIDEBAR ─┐  ┌─ CONTENT PANEL ────────────────────────────┐  │
│  │            │  │                                             │  │
│  │ 🎨 General │  │  APPEARANCE                                │  │
│  │            │  │  ┌────────────────────────────────────┐    │  │
│  │ 🎬 Video   │  │  │ Theme:  ◉ System  ○ Light  ○ Dark  │    │  │
│  │            │  │  └────────────────────────────────────┘    │  │
│  │ 🔊 Audio   │  │                                             │  │
│  │            │  │  COLOR ACCENT                               │  │
│  │ 📝 Subtitles│ │  ┌──────────────────────────────────────┐  │  │
│  │            │  │  │  [🔵] Blue   [🟣] Purple  [🟢] Green │  │  │
│  │ ⌨ Shortcuts│  │  │  [🟠] Orange [🔴] Red    [⚫] Mono  │  │  │
│  │            │  │  └──────────────────────────────────────┘  │  │
│  │ 🌐 Network │  │                                             │  │
│  │            │  │  STARTUP                                    │  │
│  │ 🔧 Advanced│  │  ☑ Remember last window size               │  │
│  │            │  │  ☑ Resume playback from last position      │  │
│  └────────────┘  │  ☐ Start minimized                         │  │
│                  │  ☑ Check for updates automatically          │  │
│                  │                                             │  │
│                  │  PERFORMANCE                                │  │
│                  │  Hardware Acceleration: [✓] Enabled        │  │
│                  │  ┌────────────────────────────────────┐    │  │
│                  │  │ GPU: NVIDIA GeForce RTX 3060       │    │  │
│                  │  │ Status: ✓ Active                   │    │  │
│                  │  └────────────────────────────────────┘    │  │
│                  │                                             │  │
│                  └─────────────────────────────────────────────┘  │
│                                                                    │
│                                   [Cancel]  [Apply]  [Save]       │
└───────────────────────────────────────────────────────────────────┘

COLOR NOTES:
- Sidebar: Light grey background with blue selection highlight
- Active tab: Gradient left border (4px) + subtle background tint
- Toggle switches: Animated slide with gradient fill
- Color swatches: Large circular buttons with hover glow
- Save button: Vibrant gradient (blue → purple)
```

#### 3.1.0.5 Visual States & Animations

**Loading States:**
```
┌─────────────────────────────────────────┐
│                                         │
│          ⟳                              │ ← Spinning gradient ring
│       Loading...                        │    (blue → purple)
│                                         │
│   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░           │ ← Progress bar with shimmer
│        Loading media: 75%               │    
│                                         │
└─────────────────────────────────────────┘
```

**Buffering Indicator:**
```
┌─────────────────────────────────────────┐
│                                         │
│  [Video continues playing with overlay]│
│                                         │
│     ┌─────────────────────────────┐    │
│     │  ⚡ Buffering...             │    │ ← Amber color
│     │  ▓▓▓▓▓▓▓░░░░░░░░░           │    │    Pulsing animation
│     └─────────────────────────────┘    │
│                                         │
└─────────────────────────────────────────┘
```

**Error State:**
```
┌─────────────────────────────────────────┐
│                                         │
│          ⚠                              │ ← Red color
│    Playback Error                       │
│                                         │
│  Unable to decode video stream          │
│  Codec: H.265 (HEVC) not supported     │
│                                         │
│    [Try Different Codec]  [Details]    │
│                                         │
└─────────────────────────────────────────┘
```

**Notification Toasts:**
```
  ┌──────────────────────────────────┐
  │ ✓ Playlist saved successfully    │  ← Green, slides in from top-right
  └──────────────────────────────────┘     Auto-dismiss after 3s

  ┌──────────────────────────────────┐
  │ ℹ Switched to 1080p quality      │  ← Blue, informational
  └──────────────────────────────────┘

  ┌──────────────────────────────────┐
  │ ⚠ Low disk space warning          │  ← Amber, requires action
  └──────────────────────────────────┘
```

**Volume Overlay (Temporary):**
```
        ┌──────────────────┐
        │   🔊 Volume      │
        │                  │
        │   ┃┃┃┃┃┃┃┃░░    │  ← Vertical bars with gradient
        │      75%         │
        │                  │
        └──────────────────┘
        ↑ Center of screen, fades after 1.5s
```

**Speed Indicator (Hold Click):**
```
        ┌──────────────┐
        │   ⚡ 2.0x    │  ← Purple gradient with glow
        └──────────────┘
        ↑ Top-right during hold
```

#### 3.1.0.6 Interactive Elements Design

**Button States:**
- **Normal**: Soft shadow, brand color
- **Hover**: Scale 1.05, brighter color, glow effect
- **Active/Pressed**: Scale 0.95, deeper color
- **Disabled**: 50% opacity, no interaction
- **Focus**: Blue ring outline (2px)

**Slider Design:**
- Track: 4px height, rounded, gradient background
- Thumb: 16px circle, white with shadow, hover = scale 1.2
- Fill: Animated gradient (blue → purple)
- Tooltip: Shows value on hover with smooth fade-in

**Toggle Switches:**
- Off: Grey background, white knob on left
- On: Gradient background (blue → purple), white knob on right
- Animation: Smooth slide (200ms ease-out)
- Label: Clear text adjacent to switch

**Dropdown Menus:**
- Modern card-style with shadow
- Hover: Light background tint
- Selected: Gradient left border + checkmark
- Icons: Aligned left, colorful for visual distinction
- Smooth height animation when opening

#### 3.1.0.7 Responsive Design Breakpoints

**Full View (Default - 1280px+)**
- Video: Maximum area, 16:9 aspect maintained
- Sidebar: 280px width, always visible
- Controls: Full feature set displayed

**Compact View (800px - 1279px)**
- Video: Slightly reduced
- Sidebar: Collapsible (toggle button)
- Controls: Icon-only for secondary features

**Minimal View (< 800px)**
- Video: Maximum available space
- Sidebar: Overlay mode (slides over video)
- Controls: Essential only, nested menus for advanced

#### 3.1.0.8 Professional Polish Features

**CEO Demo Ready Elements:**
1. **Splash Screen**: Animated logo with gradient, professional fade-in
2. **First Launch Tutorial**: Optional interactive tour with highlights
3. **Smooth Transitions**: All state changes use easing curves (ease-out)
4. **Micro-interactions**: Subtle hover effects, button bounces, smooth scrolling
5. **Loading Skeleton**: No white flashes, graceful content loading
6. **Haptic Feedback**: Optional vibration on supported devices
7. **Sound Effects**: Subtle audio cues (optional, off by default)
8. **Gesture Support**: Swipe gestures on touchpads/touchscreens
9. **Performance Metrics**: Optional FPS counter for technical demos
10. **Brand Consistency**: Logo, colors, typography unified throughout

**Accessibility (Professional Standard):**
- High contrast mode with WCAG AA compliance
- Screen reader optimized labels
- Keyboard navigation with visible focus indicators
- Reduced motion option for animations
- Scalable text (up to 200%)
- Clear error messages with recovery steps

### 3.1.1 Main Window Components
- **Menu Bar**:
  - File: Open File, Open Folder, Open URL, Recent Files, Quit
  - Playback: Play/Pause, Stop, Previous, Next, Jump to Time
  - Audio: Audio Track, Volume, Audio Device, Audio Effects
  - Video: Video Track, Fullscreen, Aspect Ratio, Crop, Filters
  - Subtitle: Subtitle Track, Add Subtitle File, Subtitle Delay
  - Tools: Preferences, Media Information, Codec Information, Playlist
  - View: Minimal View, Compact View, Advanced Controls, Playlist
  - Help: About, Check for Updates, Documentation

- **Video Display Area**:
  - Central widget occupying majority of window
  - Maintains aspect ratio of video
  - Double-click to toggle fullscreen
  - Right-click context menu for quick actions
  - Overlay controls (fade out after 3 seconds of inactivity)
  - Visual feedback for volume/seeking

- **Control Panel** (Bottom of window):
  - Play/Pause button (space bar shortcut)
  - Stop button
  - Previous track button
  - Next track button
  - Progress bar/timeline (clickable for seeking)
    - Current time display (00:00)
    - Total duration display (00:00)
    - Thumbnail preview on hover
  - Volume slider (vertical or horizontal)
  - Mute button
  - Fullscreen toggle button
  - Playlist toggle button
  - Loop mode button (no loop, loop one, loop all)
  - Shuffle button
  - Playback speed button (0.25x to 2.0x)

- **Sidebar/Dock Panel** (Collapsible):
  - Playlist view with drag-and-drop reordering
  - Media library/favorites
  - Recently played files
  - Bookmarks/chapters

#### 3.1.2 Additional Windows/Dialogs
- **Preferences/Settings Window**:
  - General: Language, theme, startup behavior
  - Video: Output module, hardware acceleration, deinterlacing
  - Audio: Output device, audio passthrough, normalization
  - Subtitles: Font, size, color, encoding, position
  - Input/Codecs: File caching, network caching, hardware acceleration
  - Interface: Look and feel, hotkeys customization
  - Playlist: Auto-play next, remember position

- **Media Information Window**:
  - General: Title, Artist, Album, Genre, Year, Description
  - Codec Details: Video/Audio codec, bitrate, resolution, framerate
  - Metadata: File size, duration, location

- **Playlist Window**:
  - List view with columns: Title, Duration, Artist, Album
  - Search/filter functionality
  - Save/Load playlist (.m3u, .pls formats)
  - Drag-and-drop support
  - Right-click context menu (remove, move up/down, play)

- **Equalizer Window**:
  - 10-band graphic equalizer
  - Presets (Rock, Jazz, Classical, etc.)
  - Custom presets saving

- **Video/Audio Effects Window**:
  - Video adjustments: Brightness, Contrast, Saturation, Gamma
  - Video effects: Sharpen, Blur, Rotate, Mirror
  - Audio effects: Equalizer, Spatializer, Compressor

#### 3.1.3 GUI Frameworks
- **Primary**: PyQt6 or PySide6 (Qt for Python)
  - Pros: Cross-platform, mature, feature-rich, excellent documentation
  - Native look and feel on both macOS and Windows
  - Hardware-accelerated rendering
  - Comprehensive widget library

- **Alternative**: Tkinter with custom widgets
  - Pros: Built-in with Python, lightweight
  - Cons: Limited styling, less modern appearance

- **Modern Alternative**: Dear PyGui
  - Pros: GPU-accelerated, modern look, performant
  - Cons: Less mature, smaller community

**Recommendation**: PyQt6/PySide6 for professional quality and feature completeness

#### 3.1.4 Theming & Styling
- **Built-in Themes**:
  - Light theme (default)
  - Dark theme
  - System theme (follows OS preference)
  - High contrast theme (accessibility)

- **Customizable Elements**:
  - Color scheme
  - Icon set
  - Font family and size
  - Window transparency/opacity
  - Control button styles

### 3.2 Playback Controls & Features

#### 3.2.1 Basic Playback Controls
- **Play/Pause**: Space bar
- **Stop**: S key
- **Previous track**: P key
- **Next track**: N key
- **Seek forward**: 
  - Right arrow: 5 seconds forward
  - Shift+Right arrow: 60 seconds forward
  - Ctrl+Right arrow: 10 seconds forward
- **Seek backward**: 
  - Left arrow: 5 seconds backward
  - Shift+Left arrow: 60 seconds backward
  - Ctrl+Left arrow: 10 seconds backward
- **Jump to specific time**: Ctrl+T or Cmd+T (macOS)
- **Frame-by-frame forward**: E key or . (period)
- **Frame-by-frame backward**: Shift+E key or , (comma)
- **Toggle hold for 2x speed**: Hold Left Click on video (YouTube-style)
  - While holding, playback speed increases to 2.0x
  - Release to return to normal speed
  - Visual indicator showing 2x speed is active

#### 3.2.2 Volume & Audio Controls
- **Volume up**: Up arrow (increase by 5%)
- **Volume down**: Down arrow (decrease by 5%)
- **Mute/Unmute**: M key
- **Volume range**: 0% to 200% (with amplification)
- **Audio track selection**: B key (cycle through audio tracks)
- **Audio device selection**: Shift+A (if multiple outputs available)
- **Audio delay adjustment**: 
  - J key: Decrease audio delay by 50ms
  - K key: Increase audio delay by 50ms
  - Reset: Shift+K

#### 3.2.3 Video Controls
- **Fullscreen toggle**: 
  - F key
  - F11 key
  - Double-click on video
  - Cmd+F (macOS) / Ctrl+F (Windows)
- **Exit fullscreen**: ESC key
- **Aspect ratio cycling**: A key
- **Aspect ratio selection**:
  - Default (original)
  - 16:9
  - 4:3
  - 1:1 (square)
  - 16:10
  - 2.35:1 (cinemascope)
  - Custom
- **Crop modes**: C key (cycle through crop modes)
- **Zoom in**: Z key or + key
- **Zoom out**: Shift+Z or - key
- **Reset zoom**: Shift+Z (when already at default)
- **Rotate clockwise**: R key
- **Rotate counter-clockwise**: Shift+R
- **Flip horizontal**: H key
- **Flip vertical**: Shift+H
- **Deinterlacing toggle**: D key
- **Video track selection**: V key (cycle through video tracks)
- **Always on top**: T key
- **Video effects/filters**: E key (open effects window)

#### 3.2.4 Playback Speed Control
- **Speed range**: 0.25x to 4.0x
- **Presets**: 0.25x, 0.5x, 0.75x, 1.0x, 1.25x, 1.5x, 2.0x, 4.0x
- **Increase speed**: ] (right bracket) - increment by 0.1x
- **Decrease speed**: [ (left bracket) - decrement by 0.1x
- **Reset to normal speed**: = (equals) or Backspace
- **Pitch correction toggle**: Shift+A (maintain audio pitch at different speeds)
- **Quick speed presets**:
  - 1 key: 0.5x speed
  - 2 key: 1.0x speed (normal)
  - 3 key: 1.5x speed
  - 4 key: 2.0x speed

#### 3.2.5 Subtitle Controls
- **Enable/Disable subtitles**: V key
- **Select subtitle track**: G key (cycle through embedded subtitle tracks)
- **Load external subtitle file**: Ctrl+S or Cmd+S (macOS)
- **Subtitle delay adjustment**:
  - H key: Delay subtitles by 50ms (show subtitles later)
  - G key: Advance subtitles by 50ms (show subtitles earlier)
  - Reset delay: Shift+H
- **Move subtitles up**: Shift+Up arrow
- **Move subtitles down**: Shift+Down arrow
- **Increase subtitle size**: Ctrl+Up arrow
- **Decrease subtitle size**: Ctrl+Down arrow
- **Font customization**: Via Preferences (family, size, color, outline)
- **Encoding selection**: Via Subtitle menu (UTF-8, Windows-1252, etc.)
- **Subtitle search/download**: Ctrl+Shift+S (OpenSubtitles integration)

#### 3.2.6 Additional Keyboard Shortcuts
- **Open file**: Ctrl+O or Cmd+O (macOS)
- **Open folder**: Ctrl+Shift+O or Cmd+Shift+O (macOS)
- **Open URL/Stream**: Ctrl+N or Cmd+N (macOS)
- **Quit application**: Ctrl+Q or Cmd+Q (macOS)
- **Take snapshot**: Shift+S (save current frame as image)
- **Record**: Ctrl+R or Cmd+R (start/stop recording)
- **Show playlist**: Ctrl+L or Cmd+L (toggle playlist view)
- **Media information**: Ctrl+I or Cmd+I (show codec/file info)
- **Equalizer**: Ctrl+E or Cmd+E (open audio equalizer)
- **Preferences/Settings**: Ctrl+P or Cmd+, (macOS)
- **Jump forward**: Ctrl+Alt+Right (jump to next chapter/bookmark)
- **Jump backward**: Ctrl+Alt+Left (jump to previous chapter/bookmark)
- **Random/Shuffle**: Ctrl+H (toggle shuffle mode)
- **Repeat mode**: Ctrl+R (cycle: off → one → all)
- **Minimal interface**: Ctrl+H (hide/show controls)
- **Compact mode**: Ctrl+M (toggle compact view)
- **Screenshot**: Shift+S (save current frame)
- **50% jump**: 5 key (jump to 50% of video)
- **Position jumps**: 
  - 0 key: Jump to 0% (beginning)
  - 1 key: Jump to 10%
  - 2 key: Jump to 20%
  - 3 key: Jump to 30%
  - 4 key: Jump to 40%
  - 5 key: Jump to 50%
  - 6 key: Jump to 60%
  - 7 key: Jump to 70%
  - 8 key: Jump to 80%
  - 9 key: Jump to 90%

#### 3.2.7 Mouse Controls
- **Single click on video**: Show/hide overlay controls
- **Double click on video**: Toggle fullscreen
- **Right click**: Context menu (quick actions)
- **Scroll wheel**: Volume control (up = increase, down = decrease)
- **Shift + Scroll wheel**: Seek forward/backward (5 seconds per scroll)
- **Click on timeline**: Seek to position
- **Drag timeline**: Scrub through video with preview
- **Hold Left Click on video**: 2x speed while held (YouTube-style)
  - Visual overlay indicator "2x" appears while held
  - Audio pitch maintained or normal based on settings
  - Instant return to normal speed on release

### 3.3 Playlist Management

#### 3.3.1 Playlist Operations
- Create new playlist
- Open existing playlist (.m3u, .m3u8, .pls, .xspf)
- Save playlist
- Add files/folders to playlist
- Remove items from playlist
- Clear entire playlist
- Drag-and-drop reordering
- Sort by: Name, Duration, Date Added, Custom Order

#### 3.3.2 Playback Modes
- Normal playback (play in order)
- Repeat one (loop current item)
- Repeat all (loop entire playlist)
- Shuffle mode (random order)
- Auto-play next item

#### 3.3.3 Playlist Features
- Search/filter within playlist
- Bookmarks (save position in video)
- Resume playback from last position
- Recently played list (persistent)
- Favorites/starred items

### 3.4 Advanced Features

#### 3.4.1 Streaming Support
- **Network Protocols**:
  - HTTP/HTTPS streaming
  - RTSP (Real-Time Streaming Protocol)
  - RTMP (Real-Time Messaging Protocol)
  - UDP/RTP streams
  - HLS (HTTP Live Streaming)
  - DASH (Dynamic Adaptive Streaming over HTTP)

- **Streaming Features**:
  - URL input dialog
  - Stream buffering with adjustable cache size
  - Network caching options (300ms to 10s)
  - Reconnection on network errors
  - Stream recording capability

#### 3.4.2 Recording & Capture
- Record streaming media to file
- Screen capture of video playback
- Audio extraction from video
- Snapshot/Screenshot capability (PNG, JPG)
- Continuous screenshot (every N seconds)

#### 3.4.3 Media Conversion
- Built-in converter for common formats
- Batch conversion support
- Codec selection
- Quality presets (low, medium, high, lossless)
- Audio extraction
- Video codec transcoding

#### 3.4.4 Chapter & Bookmark Support
- Chapter navigation (if embedded in file)
- Custom bookmarks (save specific timestamps)
- Bookmark management (edit, delete, rename)
- Jump to bookmark via hotkey

#### 3.4.5 A-B Repeat
- Set point A (start loop)
- Set point B (end loop)
- Loop between A and B continuously
- Clear A-B loop

#### 3.4.6 Casting & Remote Control
- Chromecast support
- AirPlay support (macOS)
- DLNA/UPnP streaming
- Web-based remote control interface

---

## 4. Media Format Support

### 4.1 Video Container Formats
**Priority 1 (Must Support)**:
- MP4 (.mp4, .m4v)
- MKV (.mkv)
- AVI (.avi)
- MOV (.mov)
- WMV (.wmv)
- FLV (.flv)
- WebM (.webm)
- MPEG/MPG (.mpeg, .mpg, .mpe)
- TS (.ts, .mts, .m2ts) - Transport Stream
- 3GP (.3gp, .3g2)

**Priority 2 (Should Support)**:
- OGV (.ogv, .ogg)
- VOB (.vob) - DVD files
- ASF (.asf)
- DivX (.divx)
- F4V (.f4v)
- MXF (.mxf)
- RM (.rm, .rmvb)

### 4.2 Video Codecs
**Priority 1 (Must Support)**:
- H.264 (AVC)
- H.265 (HEVC)
- VP8
- VP9
- AV1
- MPEG-4 Part 2
- MPEG-2
- MPEG-1
- Theora
- WMV (Windows Media Video)

**Priority 2 (Should Support)**:
- H.263
- DivX
- Xvid
- ProRes (macOS)
- DNxHD
- FFV1 (lossless)

### 4.3 Audio Formats
**Priority 1 (Must Support)**:
- MP3 (.mp3)
- AAC (.aac, .m4a)
- FLAC (.flac)
- WAV (.wav)
- OGG Vorbis (.ogg)
- WMA (.wma)
- ALAC (.m4a) - Apple Lossless
- Opus (.opus)
- AIFF (.aiff, .aif)

**Priority 2 (Should Support)**:
- APE (.ape) - Monkey's Audio
- DTS
- AC3 (Dolby Digital)
- EAC3 (Dolby Digital Plus)
- TrueHD
- AMR (.amr)

### 4.4 Subtitle Formats
**Must Support**:
- SRT (.srt) - SubRip
- ASS (.ass) - Advanced SubStation Alpha
- SSA (.ssa) - SubStation Alpha
- WebVTT (.vtt)
- SUB (.sub) - MicroDVD, SubViewer
- SMI (.smi) - SAMI
- VTT (.vtt)
- Embedded subtitles (in MKV, MP4, etc.)
- DVD subtitles (VOBsub)
- Closed Captions (CEA-608, CEA-708)

### 4.5 Image Formats (for slideshows/thumbnails)
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- GIF (.gif)
- TIFF (.tiff, .tif)
- WebP (.webp)

### 4.6 Playlist Formats
- M3U (.m3u, .m3u8)
- PLS (.pls)
- XSPF (.xspf)
- WPL (.wpl)
- ASX (.asx)
- CUE (.cue)

---

## 5. Cross-Platform Considerations

### 5.1 macOS-Specific Requirements

#### 5.1.1 Platform Integration
- Native macOS menubar integration
- Touch Bar support (for MacBook Pro)
- Mission Control integration
- Spaces support
- macOS notifications (media controls on lock screen)
- Dark mode support (follow system preference)
- Picture-in-Picture (PiP) support
- Retina display optimization

#### 5.1.2 Hardware Acceleration
- VideoToolbox API for hardware decoding
- Metal API for video rendering
- Core Audio for audio output
- AVFoundation integration

#### 5.1.3 File System & Permissions
- Handle macOS Gatekeeper requirements
- Request necessary permissions (media access)
- Support for macOS file tags and labels
- Spotlight metadata integration

#### 5.1.4 Distribution
- Code signing with Apple Developer certificate
- Notarization for Catalina and later
- DMG installer creation
- Optional: Mac App Store distribution

### 5.2 Windows-Specific Requirements

#### 5.2.1 Platform Integration
- Windows taskbar integration (thumbnail toolbar)
- Jump list support (recent files)
- Windows notifications
- Windows 10/11 dark mode support
- Windows Media keys support
- System tray icon with context menu

#### 5.2.2 Hardware Acceleration
- DirectX Video Acceleration (DXVA) for decoding
- Direct3D 11 for video rendering
- Windows Audio Session API (WASAPI)
- Media Foundation integration

#### 5.2.3 File System & Permissions
- Windows Registry integration (file associations)
- User Account Control (UAC) compatibility
- Support for Windows long paths
- Network path (UNC) support

#### 5.2.4 Distribution
- MSI or NSIS installer
- Digital signature with Authenticode
- Windows Defender SmartScreen compatibility
- Optional: Microsoft Store distribution

### 5.3 Unified Cross-Platform Features

#### 5.3.1 Configuration Management
- Separate config files per platform
- Common settings format (JSON or YAML)
- Settings migration between platforms
- Cloud settings sync (optional)

#### 5.3.2 File Path Handling
- Abstraction layer for path operations
- Support for both forward slashes and backslashes
- Drive letter handling (Windows)
- Case-sensitivity handling (macOS vs Windows)

#### 5.3.3 Keyboard Shortcuts
- Platform-specific modifier keys:
  - Cmd (macOS) ↔ Ctrl (Windows)
  - Option (macOS) ↔ Alt (Windows)
- Standard shortcuts per platform
- Customizable shortcuts with platform awareness

#### 5.3.4 Internationalization (i18n)
- UTF-8 support throughout application
- Locale-specific date/time formatting
- Number formatting per locale
- Language packs (English, Spanish, French, German, Chinese, Japanese, etc.)
- Right-to-left (RTL) language support

---

## 6. Non-Functional Requirements

### 6.1 Security

#### 6.1.1 Input Validation
- Validate all file paths and URLs
- Sanitize user input for playlist operations
- Check file signatures/magic numbers
- Prevent directory traversal attacks
- Limit file size for parsing operations

#### 6.1.2 Network Security
- HTTPS validation for streaming URLs
- Certificate verification
- Timeout limits for network operations
- Rate limiting for external API calls
- No execution of embedded scripts

#### 6.1.3 Privacy
- No telemetry without explicit user consent
- No tracking or analytics by default
- Local storage of user preferences
- Optional usage statistics (opt-in)
- Clear privacy policy

### 6.2 Accessibility

#### 6.2.1 Visual Accessibility
- High contrast theme
- Scalable UI (font size adjustment)
- Colorblind-friendly color schemes
- Keyboard navigation for all functions
- Focus indicators

#### 6.2.2 Audio/Visual Accessibility
- Closed caption support
- Audio descriptions (if embedded)
- Visual feedback for audio events
- Screen reader compatibility
- Adjustable subtitle appearance

### 6.3 Usability

#### 6.3.1 User Experience
- Intuitive interface (minimal learning curve)
- Consistent behavior across platforms
- Helpful tooltips
- Context-sensitive help
- Undo/Redo support where applicable

#### 6.3.2 Documentation
- User manual (online and offline)
- Video tutorials
- Keyboard shortcut reference
- FAQ section
- Troubleshooting guide

### 6.4 Reliability

#### 6.4.1 Error Handling
- Graceful degradation for unsupported formats
- Auto-recovery from crashes
- Save state before crashes
- Detailed error logs
- User-friendly error messages

#### 6.4.2 Testing Requirements
- Unit tests for all core components (>80% coverage)
- Integration tests for playback pipeline
- Performance tests (benchmark suite)
- UI tests (automated GUI testing)
- Cross-platform testing (CI/CD)
- Memory leak detection
- Stress testing with large files

### 6.5 Maintainability

#### 6.5.1 Code Documentation
- Inline comments for complex logic
- Function/class docstrings
- Architecture documentation
- API documentation
- Contribution guidelines

#### 6.5.2 Version Control
- Git repository with clear history
- Semantic versioning (MAJOR.MINOR.PATCH)
- Changelog for each release
- Branch strategy (main, develop, feature branches)
- Code review process

#### 6.5.3 Dependency Management
- Pin dependency versions
- Regular dependency updates
- Security vulnerability scanning
- License compatibility checks

---

## 7. Technology Stack Recommendations

### 7.1 Core Libraries

#### 7.1.1 GUI Framework
**Primary Choice**: PyQt6 or PySide6
- Mature, well-documented
- Cross-platform native look and feel
- Hardware-accelerated widgets
- Commercial-friendly licensing (PySide6 - LGPL)

**Installation**:
```bash
pip install PyQt6
# or
pip install PySide6
```

#### 7.1.2 Media Framework
**Primary Choice**: python-mpv (libmpv bindings)
- Based on MPV player (fork of MPlayer)
- Excellent codec support
- Hardware acceleration
- Cross-platform
- Active development

**Alternative**: python-vlc (libvlc bindings)
- Based on VLC
- Comprehensive format support
- Mature and stable

**Installation**:
```bash
pip install python-mpv
# Requires libmpv installed on system
# macOS: brew install mpv
# Windows: Download from mpv.io
```

#### 7.1.3 Audio/Video Processing
- **FFmpeg**: Format conversion, codec handling
- **PyAV**: Pythonic FFmpeg bindings
- **sounddevice**: Audio I/O
- **numpy**: Array operations for audio/video data

```bash
pip install av sounddevice numpy
```

### 7.2 Supporting Libraries

#### 7.2.1 File Handling
- **pathlib**: Path operations (built-in)
- **send2trash**: Safe file deletion
- **watchdog**: File system monitoring

```bash
pip install send2trash watchdog
```

#### 7.2.2 Network/Streaming
- **requests**: HTTP streaming
- **aiohttp**: Async HTTP requests
- **yt-dlp**: YouTube and streaming site support

```bash
pip install requests aiohttp yt-dlp
```

#### 7.2.3 Metadata & Subtitles
- **mutagen**: Audio metadata
- **pymediainfo**: Media file information
- **pysrt**: SRT subtitle parsing
- **pysubs2**: Advanced subtitle formats

```bash
pip install mutagen pymediainfo pysrt pysubs2
```

#### 7.2.4 Configuration & Data
- **pyyaml**: YAML configuration files
- **python-dotenv**: Environment variables
- **platformdirs**: Platform-specific directories

```bash
pip install pyyaml python-dotenv platformdirs
```

#### 7.2.5 Testing & Quality
- **pytest**: Testing framework
- **pytest-qt**: Qt testing
- **pytest-cov**: Coverage reporting
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking

```bash
pip install pytest pytest-qt pytest-cov black flake8 mypy
```

### 7.3 Platform-Specific Libraries

#### 7.3.1 macOS
- **pyobjc**: macOS native API access
- **AppKit**: macOS UI integration

```bash
pip install pyobjc-framework-Cocoa
```

#### 7.3.2 Windows
- **pywin32**: Windows API access
- **winreg**: Windows registry (built-in)

```bash
pip install pywin32
```

### 7.4 Development Tools

#### 7.4.1 Build & Packaging
- **PyInstaller**: Executable creation
- **py2app**: macOS app bundling
- **cx_Freeze**: Alternative packager

```bash
pip install pyinstaller py2app cx_Freeze
```

#### 7.4.2 Documentation
- **Sphinx**: Documentation generation
- **mkdocs**: Markdown documentation

```bash
pip install sphinx mkdocs
```

---

## 8. Distribution & Deployment Strategy

### 8.1 Target Platform (MVP)

**Initial Release: Windows Only**
- Windows 10 (64-bit)
- Windows 11 (64-bit)
- Minimum: 4GB RAM, 500MB disk space
- No installation required (portable executable)

**Future Platforms:**
- macOS (Phase 2)
- Linux (Phase 3)

### 8.2 Packaging Strategy

#### 8.2.1 Single-File Executable (Primary Distribution)

**Tool: PyInstaller**
- Creates standalone `.exe` with all dependencies bundled
- No Python installation required on user's machine
- No installation wizard needed - just download and run

**Build Command:**
```bash
pyinstaller --onefile \
  --windowed \
  --name "PyMediaPlayer" \
  --icon=resources/app_icon.ico \
  --add-data "resources;resources" \
  --add-data "themes;themes" \
  --hidden-import=PyQt6 \
  --hidden-import=mpv \
  --noconsole \
  main.py
```

**Build Flags Explained:**
- `--onefile`: Single executable file (no DLL hell)
- `--windowed`: No console window (GUI-only)
- `--name`: Output filename
- `--icon`: Application icon (.ico format)
- `--add-data`: Include resource files (syntax: "source;destination")
- `--hidden-import`: Ensure dynamic imports are included
- `--noconsole`: Hide terminal window

**Output:**
- Location: `dist/PyMediaPlayer.exe`
- Size: ~50-80MB (includes Python runtime + all dependencies)
- Self-contained: No external dependencies needed

#### 8.2.2 ZIP Package (Secondary Distribution)

**Package Structure:**
```
PyMediaPlayer-v1.0.0-Windows-x64.zip
├── PyMediaPlayer.exe               # Main executable
├── README.txt                      # Quick start guide
├── LICENSE.txt                     # MIT/GPL License
├── CHANGELOG.txt                   # Version history
└── TROUBLESHOOTING.txt            # Common issues & solutions
```

**README.txt Template:**
```
   PyMedia Player v1.0.0 - Windows

QUICK START
-----------
1. Extract all files from this ZIP
2. Double-click PyMediaPlayer.exe
3. Start playing your media!

FIRST RUN
---------
Windows SmartScreen may show a warning on first run:
1. Click "More info"
2. Click "Run anyway"

This is normal for new software without an expensive code signing certificate.
The app is safe and open-source.

SYSTEM REQUIREMENTS
-------------------
- Windows 10/11 (64-bit)
- 4GB RAM (minimum)
- 500MB free disk space

SUPPORTED FORMATS
-----------------
Video: MP4, MKV, AVI, MOV, WMV, FLV, WebM, TS
Audio: MP3, AAC, FLAC, WAV, OGG, WMA, ALAC
Subtitles: SRT, ASS, SSA, VTT, SUB

NEED HELP?
----------
GitHub: https://github.com/yourusername/pymedia-player
Issues: https://github.com/yourusername/pymedia-player/issues
Docs: https://github.com/yourusername/pymedia-player/wiki

KEYBOARD SHORTCUTS
------------------
Space    - Play/Pause
F        - Fullscreen
M        - Mute
←/→      - Seek backward/forward 5s
↑/↓      - Volume up/down
Ctrl+O   - Open file

For complete keyboard shortcuts, press F1 in the app.
```

### 8.3 GitHub Releases Distribution

#### 8.3.1 Release Workflow

**1. Build Process**
```bash
# Clean previous builds
rm -rf build dist

# Create virtual environment for clean build
python -m venv build_env
source build_env/bin/activate  # On Windows: build_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build executable
pyinstaller build.spec  # Using spec file for consistent builds

# Test the executable
cd dist
./PyMediaPlayer.exe  # Verify it works
```

**2. Create ZIP Package**
```bash
cd dist
mkdir PyMediaPlayer-v1.0.0-Windows-x64
cp PyMediaPlayer.exe PyMediaPlayer-v1.0.0-Windows-x64/
cp ../README.txt PyMediaPlayer-v1.0.0-Windows-x64/
cp ../LICENSE.txt PyMediaPlayer-v1.0.0-Windows-x64/
cp ../CHANGELOG.txt PyMediaPlayer-v1.0.0-Windows-x64/
cp ../TROUBLESHOOTING.txt PyMediaPlayer-v1.0.0-Windows-x64/
zip -r PyMediaPlayer-v1.0.0-Windows-x64.zip PyMediaPlayer-v1.0.0-Windows-x64/
```

**3. Create GitHub Release**
- Navigate to: `https://github.com/username/pymedia-player/releases/new`
- Tag version: `v1.0.0` (follow semantic versioning)
- Release title: `PyMedia Player v1.0.0 - Initial Release`
- Description: Include feature list, screenshots, known issues
- Upload assets:
  - `PyMediaPlayer.exe` (standalone executable)
  - `PyMediaPlayer-v1.0.0-Windows-x64.zip` (package with docs)
  - `SHA256SUMS.txt` (checksums for verification)

**4. Generate Checksums**
```bash
# Windows (PowerShell)
Get-FileHash PyMediaPlayer.exe -Algorithm SHA256 > SHA256SUMS.txt
Get-FileHash PyMediaPlayer-v1.0.0-Windows-x64.zip -Algorithm SHA256 >> SHA256SUMS.txt

# Linux/Mac
sha256sum PyMediaPlayer.exe > SHA256SUMS.txt
sha256sum PyMediaPlayer-v1.0.0-Windows-x64.zip >> SHA256SUMS.txt
```

#### 8.3.2 Release Template

```markdown
# PyMedia Player v1.0.0 - Initial Release 🎬

## What's New
- Full-featured media player for Windows
- Support for 30+ video/audio formats
- VLC-style keyboard shortcuts
- Beautiful dark/light themes
- Playlist management
- Hardware acceleration support

## Download

### Standalone Executable (Recommended)
**[Download PyMediaPlayer.exe](link)** (52 MB)
- No installation required
- Just download and run!

### Complete Package
**[Download PyMediaPlayer-v1.0.0-Windows-x64.zip](link)** (52 MB)
- Includes README and documentation
- Recommended for first-time users

## System Requirements
- Windows 10/11 (64-bit)
- 4GB RAM minimum
- 500MB free disk space

## Known Issues
- Windows SmartScreen warning on first run (click "More info" → "Run anyway")
- Subtitle font customization requires app restart
- 4K playback may stutter on older GPUs (use software decoding)

## Verification
SHA256 checksums:
```
[checksum here] PyMediaPlayer.exe
[checksum here] PyMediaPlayer-v1.0.0-Windows-x64.zip
```

## Installation
1. Download the `.exe` or `.zip`
2. Extract (if using ZIP)
3. Double-click `PyMediaPlayer.exe`
4. Done! 🎉

## First Run
If Windows shows a security warning:
1. Click "More info"
2. Click "Run anyway"

This is normal for new applications. We're working on code signing to remove this warning.

## Documentation
- [User Guide](link)
- [Keyboard Shortcuts](link)
- [FAQ](link)
- [Report Bug](link)

## What's Next
- v1.1.0: Subtitle search integration
- v1.2.0: Streaming improvements
- v2.0.0: macOS support

---
Full changelog: [CHANGELOG.md](link)
```

### 8.4 Antivirus False Positive Mitigation

#### 8.4.1 Prevention Strategies (No Code Signing)

**A. VirusTotal Submission**
- Upload `.exe` to https://virustotal.com immediately after build
- Monitor detection rates
- If false positives appear, submit to vendors:
  - Microsoft Defender: https://www.microsoft.com/en-us/wdsi/filesubmission
  - Malwarebytes: https://www.malwarebytes.com/false-positives
  - Avast: https://www.avast.com/false-positive-file-form.php

**B. Build Hygiene**
- Use official Python from python.org
- Build on clean Windows VM (no malware)
- Use official packages from PyPI only
- Document build process for reproducibility

**C. Community Trust Building**
- Open source the code (GitHub)
- Document build process in README
- Encourage users to build from source
- Collect 20-50 downloads to build Windows SmartScreen reputation

**D. User Communication**
```markdown
## Security Notice

PyMedia Player is safe and open-source. You can verify by:

1. **Scan with VirusTotal**: [Link to scan results]
2. **Review source code**: All code is on GitHub
3. **Build from source**: Follow our build guide
4. **Check community**: Read reviews and issues

### Windows SmartScreen Warning
Windows shows warnings for new apps without expensive certificates ($200/year).
This is normal and doesn't mean the app is unsafe.

Click "More info" → "Run anyway" to continue.
```

#### 8.4.2 Windows SmartScreen Handling

**User Experience:**
```
Download → Run → SmartScreen Warning → "More info" → "Run anyway" → App Launches
```

**Documentation:**
- Create animated GIF showing the process
- Add to README and release notes
- Explain why warning appears
- Mention code signing is planned for future

### 8.5 Build Automation

#### 8.5.1 Build Script (build.py)

```python
#!/usr/bin/env python3
"""
Automated build script for PyMedia Player
Handles cleaning, building, packaging, and verification
"""

import os
import shutil
import subprocess
import hashlib
from pathlib import Path

VERSION = "1.0.0"
APP_NAME = "PyMediaPlayer"

def clean():
    """Remove previous build artifacts"""
    for dir in ['build', 'dist', '__pycache__']:
        if os.path.exists(dir):
            shutil.rmtree(dir)
    print("✓ Cleaned build directories")

def build_executable():
    """Build standalone executable"""
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        f'--name={APP_NAME}',
        '--icon=resources/app_icon.ico',
        'main.py'
    ]
    subprocess.run(cmd, check=True)
    print(f"✓ Built {APP_NAME}.exe")

def create_package():
    """Create ZIP package with documentation"""
    package_name = f"{APP_NAME}-v{VERSION}-Windows-x64"
    package_dir = Path('dist') / package_name
    
    # Create directory structure
    package_dir.mkdir(exist_ok=True)
    
    # Copy files
    shutil.copy(f'dist/{APP_NAME}.exe', package_dir)
    shutil.copy('README.txt', package_dir)
    shutil.copy('LICENSE.txt', package_dir)
    shutil.copy('CHANGELOG.txt', package_dir)
    
    # Create ZIP
    shutil.make_archive(str(package_dir), 'zip', package_dir)
    print(f"✓ Created {package_name}.zip")

def generate_checksums():
    """Generate SHA256 checksums"""
    files = [
        f'dist/{APP_NAME}.exe',
        f'dist/{APP_NAME}-v{VERSION}-Windows-x64.zip'
    ]
    
    with open('dist/SHA256SUMS.txt', 'w') as f:
        for filepath in files:
            sha256 = hashlib.sha256()
            with open(filepath, 'rb') as file:
                sha256.update(file.read())
            f.write(f"{sha256.hexdigest()}  {Path(filepath).name}\n")
    
    print("✓ Generated SHA256 checksums")

def main():
    print(f"Building {APP_NAME} v{VERSION}...")
    clean()
    build_executable()
    create_package()
    generate_checksums()
    print(f"\n✅ Build complete! Files in dist/")

if __name__ == '__main__':
    main()
```

#### 8.5.2 PyInstaller Spec File (build.spec)

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resources', 'resources'),
        ('themes', 'themes'),
    ],
    hiddenimports=[
        'PyQt6',
        'mpv',
        'av',
        'mutagen',
        'pysrt',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PyMediaPlayer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/app_icon.ico',
)
```

### 8.6 Version Management

**Semantic Versioning (SemVer):**
- Format: `MAJOR.MINOR.PATCH` (e.g., 1.0.0)
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

**Version Numbering Plan:**
- v1.0.0: Initial MVP release (Windows only)
- v1.1.0: Bug fixes + subtitle improvements
- v1.2.0: Streaming enhancements
- v1.5.0: Major feature additions
- v2.0.0: macOS support
- v3.0.0: Linux support

### 8.7 Update Strategy (Future)

**Planned for v1.2.0+:**
- In-app update checker
- Compares current version with latest GitHub release
- One-click download and install
- Automatic backup of settings

**Update Check Flow:**
```
App Launch → Check GitHub API → New version available? → Show notification → Download → Install → Restart
```

### 8.8 Distribution Metrics

**Track via GitHub:**
- Download counts (per release)
- Geographic distribution
- Release asset statistics
- Star/fork growth

**Future Analytics:**
- Optional opt-in telemetry
- Crash reporting (with user consent)
- Feature usage statistics
- Performance metrics

---

## 9. Development Phases & Milestones

### Phase 1: Foundation (Weeks 1-2)
- [ ] Set up project structure
- [ ] Configure development environment
- [ ] Create basic GUI shell (main window, menu bar)
- [ ] Implement configuration management
- [ ] Set up logging system

### Phase 2: Core Playback (Weeks 3-5)
- [ ] Integrate libmpv/libvlc
- [ ] Implement basic playback controls (play, pause, stop)
- [ ] Add progress bar and seeking
- [ ] Implement volume control
- [ ] Add video rendering widget

### Phase 3: Format Support (Weeks 6-7)
- [ ] File open dialog
- [ ] Format detection
- [ ] Codec handling
- [ ] Error handling for unsupported formats
- [ ] Test with various file types

### Phase 4: Advanced Controls (Weeks 8-9)
- [ ] Playback speed control
- [ ] Audio track selection
- [ ] Video track selection
- [ ] Subtitle support (embedded and external)
- [ ] Aspect ratio and video effects

### Phase 5: Playlist (Weeks 10-11)
- [ ] Playlist UI
- [ ] Add/remove items
- [ ] Drag-and-drop reordering
- [ ] Playlist save/load
- [ ] Playback modes (repeat, shuffle)

### Phase 6: Advanced Features (Weeks 12-14)
- [ ] Streaming support
- [ ] Equalizer
- [ ] Video/audio effects
- [ ] A-B repeat
- [ ] Bookmarks
- [ ] Screen capture/recording

### Phase 7: Cross-Platform (Weeks 15-16)
- [ ] macOS-specific features
- [ ] Windows-specific features
- [ ] Platform testing
- [ ] Installer creation
- [ ] Code signing

### Phase 8: Polish & Release (Weeks 17-18)
- [ ] UI refinements
- [ ] Performance optimization
- [ ] Bug fixes
- [ ] Documentation
- [ ] User manual
- [ ] Beta testing
- [ ] Final release

---

## 9. Success Criteria

### 9.1 Functional Success
- ✓ Plays all major video/audio formats
- ✓ Subtitle support (embedded and external)
- ✓ Streaming from URLs
- ✓ Playlist management
- ✓ Cross-platform (macOS & Windows)

### 9.2 Performance Success
- ✓ 60 FPS playback for 1080p video
- ✓ < 2 second startup time
- ✓ < 500ms seeking response
- ✓ < 500MB RAM for 1080p playback

### 9.3 Quality Success
- ✓ 80%+ test coverage
- ✓ PEP 8 compliant
- ✓ No critical bugs
- ✓ Comprehensive documentation

### 9.4 User Success
- ✓ Intuitive interface (user testing)
- ✓ Positive user feedback
- ✓ Active usage and adoption
- ✓ Community contributions

---

## 10. Risks & Mitigation

### 10.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Codec compatibility issues | High | Medium | Use mature libraries (libmpv/libvlc), extensive testing |
| Performance issues on older hardware | Medium | Medium | Hardware acceleration, software fallback, optimization |
| Cross-platform GUI inconsistencies | Medium | Low | Use Qt framework, platform-specific testing |
| Memory leaks in long playback | High | Medium | Profiling, regular cleanup, automated tests |
| Third-party library dependencies | Medium | Medium | Pin versions, regular updates, fallback options |

### 10.2 Project Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Scope creep | High | High | Strict prioritization, MVP focus, phased approach |
| Insufficient testing | High | Medium | Automated testing, CI/CD, beta testing program |
| Platform-specific bugs | Medium | Medium | Regular cross-platform builds, diverse testing |
| Documentation lag | Low | High | Write docs alongside code, documentation sprints |

---

## 11. Future Enhancements (Post-MVP)

### 11.1 Advanced Features
- Video editing capabilities (trim, merge)
- Media library with tagging
- Online content integration (YouTube, Vimeo)
- Chromecast/AirPlay support
- VR video playback (180°/360°)
- Audio visualization
- Voice control

### 11.2 Social Features
- Share watching sessions (watch party)
- Social media integration
- Collaborative playlists
- Comments/annotations

### 11.3 Technical Enhancements
- GPU-accelerated video filters
- Machine learning features (auto-subtitles, scene detection)
- HDR support
- Dolby Atmos support
- Linux support

---

## 12. References & Resources

### 12.1 Similar Projects
- VLC Media Player: https://www.videolan.org/vlc/
- MPV Player: https://mpv.io/
- MPC-HC: https://mpc-hc.org/

### 12.2 Documentation
- PyQt6 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt6/
- python-mpv: https://github.com/jaseg/python-mpv
- FFmpeg Documentation: https://ffmpeg.org/documentation.html

### 12.3 Standards
- MPEG Standards: https://mpeg.chiariglione.org/
- WebM Project: https://www.webmproject.org/
- Matroska Specification: https://www.matroska.org/

---

**Document Version**: 1.0  
**Last Updated**: January 2025  
**Author**: Development Team  
**Status**: Ready for Review
