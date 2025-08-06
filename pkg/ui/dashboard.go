package ui

import (
	"fmt"
	"sync"
	"time"

	"github.com/duncan/essayforge/pkg/models"
	"github.com/fatih/color"
	"strings"
)

// Dashboard manages the terminal UI for progress tracking
type Dashboard struct {
	mu              sync.Mutex
	progress        models.Progress
	agentStatuses   map[string]AgentStatus
	startTime       time.Time
	refreshInterval time.Duration
}

// AgentStatus tracks individual agent progress
type AgentStatus struct {
	ID        string
	Type      string
	Status    string // running, completed, failed
	StartTime time.Time
	EndTime   time.Time
	Tokens    int
}

// NewDashboard creates a new progress dashboard
func NewDashboard() *Dashboard {
	return &Dashboard{
		agentStatuses:   make(map[string]AgentStatus),
		startTime:       time.Now(),
		refreshInterval: 100 * time.Millisecond,
	}
}

// Start begins the dashboard display
func (d *Dashboard) Start() {
	// Clear screen
	fmt.Print("\033[2J\033[H")
	
	go d.refreshLoop()
}

// UpdateProgress updates the overall progress
func (d *Dashboard) UpdateProgress(progress models.Progress) {
	d.mu.Lock()
	defer d.mu.Unlock()
	d.progress = progress
}

// UpdateAgent updates a specific agent's status
func (d *Dashboard) UpdateAgent(agentID, agentType, status string, tokens int) {
	d.mu.Lock()
	defer d.mu.Unlock()
	
	agent := d.agentStatuses[agentID]
	agent.ID = agentID
	agent.Type = agentType
	agent.Status = status
	agent.Tokens = tokens
	
	if agent.StartTime.IsZero() {
		agent.StartTime = time.Now()
	}
	
	if status == "completed" || status == "failed" {
		agent.EndTime = time.Now()
	}
	
	d.agentStatuses[agentID] = agent
}

// refreshLoop continuously updates the display
func (d *Dashboard) refreshLoop() {
	ticker := time.NewTicker(d.refreshInterval)
	defer ticker.Stop()
	
	for range ticker.C {
		d.render()
	}
}

// render displays the current dashboard state
func (d *Dashboard) render() {
	d.mu.Lock()
	defer d.mu.Unlock()
	
	// Clear screen and move cursor to top
	fmt.Print("\033[2J\033[H")
	
	// Title
	titleColor := color.New(color.FgCyan, color.Bold)
	titleColor.Println("🚀 Parallel Research CLI - Progress Dashboard")
	fmt.Println(strings.Repeat("═", 60))
	
	// Overall progress
	elapsed := time.Since(d.startTime)
	fmt.Printf("📊 Stage: %s | Progress: %.1f%% | Time: %s\n",
		d.progress.Stage,
		d.progress.Percentage,
		elapsed.Round(time.Second))
	
	// Progress bar
	d.renderProgressBar(d.progress.Percentage)
	
	// Stats
	fmt.Printf("\n📈 Statistics:\n")
	fmt.Printf("   Active Agents: %d/%d\n", d.progress.ActiveAgents, len(d.agentStatuses))
	fmt.Printf("   Tokens Used: %d\n", d.progress.TokensUsed)
	fmt.Printf("   Estimated Cost: $%.2f\n", d.progress.EstimatedCost)
	
	// Agent status table
	fmt.Printf("\n🤖 Agent Status:\n")
	fmt.Println(strings.Repeat("-", 60))
	fmt.Printf("%-20s %-15s %-10s %-10s\n", "Agent Type", "Status", "Tokens", "Duration")
	fmt.Println(strings.Repeat("-", 60))
	
	// Sort agents by type for consistent display
	for _, agent := range d.agentStatuses {
		statusColor := d.getStatusColor(agent.Status)
		duration := d.getAgentDuration(agent)
		
		statusColor.Printf("%-20s %-15s %-10d %-10s\n",
			agent.Type,
			agent.Status,
			agent.Tokens,
			duration)
	}
	
	// Current message
	if d.progress.Message != "" {
		fmt.Printf("\n💬 %s\n", d.progress.Message)
	}
}

// renderProgressBar displays a visual progress bar
func (d *Dashboard) renderProgressBar(percentage float64) {
	barWidth := 50
	filled := int(percentage / 100 * float64(barWidth))
	
	fmt.Print("[")
	
	// Filled portion
	color.New(color.FgGreen).Print(strings.Repeat("█", filled))
	
	// Empty portion
	fmt.Print(strings.Repeat("░", barWidth-filled))
	
	fmt.Printf("] %.1f%%", percentage)
}

// getStatusColor returns the appropriate color for a status
func (d *Dashboard) getStatusColor(status string) *color.Color {
	switch status {
	case "running":
		return color.New(color.FgYellow)
	case "completed":
		return color.New(color.FgGreen)
	case "failed":
		return color.New(color.FgRed)
	default:
		return color.New(color.FgWhite)
	}
}

// getAgentDuration calculates how long an agent has been running
func (d *Dashboard) getAgentDuration(agent AgentStatus) string {
	if agent.StartTime.IsZero() {
		return "-"
	}
	
	endTime := agent.EndTime
	if endTime.IsZero() {
		endTime = time.Now()
	}
	
	duration := endTime.Sub(agent.StartTime)
	return duration.Round(time.Second).String()
}

// Close cleans up the dashboard
func (d *Dashboard) Close() {
	// Clear screen one final time
	fmt.Print("\033[2J\033[H")
}