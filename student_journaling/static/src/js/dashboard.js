/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, xml } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class SelfHelpDashboard extends Component {
    setup() {
        this.actionService = useService("action");
    }

    _onOpenJournaling() {
        this.actionService.doAction("student_journaling.action_student_journal");
    }

    _onOpenTips() {
        this.actionService.doAction("self_help_tips.action_self_help_tips");
    }
}

SelfHelpDashboard.template = xml`
    <div class="o_self_help_dashboard">
        <div class="dashboard-header">
            <h2>Self-Help Tools</h2>
            <p>Latihan ringan untuk menenangkan pikiran</p>
        </div>
        <div class="tools-container">
            <!-- Journaling Card -->
            <div class="tool-card card-journaling" t-on-click="_onOpenJournaling">
                <div class="card-content">
                    <h3>Journaling</h3>
                    <p>Ungkapkan pikiran dan perasaanmu dengan bebas.</p>
                </div>
                <div class="illustration">
                    <img src="/student_journaling/static/src/img/journal_book.png" style="width:100%; height:100%; object-fit:contain;"/>
                </div>
            </div>

            <!-- Tips Card -->
            <div class="tool-card card-tips" t-on-click="_onOpenTips">
                <div class="card-content">
                    <h3>Tips Self-Help</h3>
                    <p>Temukan artikel yang tepat untukmu.</p>
                </div>
                <div class="illustration">
                    <img src="/student_journaling/static/src/img/tips_phone.png" style="width:100%; height:100%; object-fit:contain;"/>
                </div>
            </div>
        </div>
    </div>
`;

registry.category("actions").add("student_journaling.self_help_dashboard", SelfHelpDashboard);
