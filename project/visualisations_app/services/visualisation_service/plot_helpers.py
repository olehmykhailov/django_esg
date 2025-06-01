import matplotlib.pyplot as plt

def format_dashboard_plot(fig, ax, title, xlabel="", ylabel_left="", axis_color_left="#000000", suptitle_mode=False):
    fig.patch.set_facecolor("#F9FAFB")
    ax.set_facecolor("#FFFFFF")
    if suptitle_mode:
        fig.suptitle(title, x=0.01, y=0.98, ha='left', fontsize=18, color="#374151", weight='medium')
    else:
        ax.set_title(title, loc='left', fontsize=16, color="#374151", weight='medium', pad=15)
    ax.set_xlabel(xlabel, fontsize=11, color="#6B7280", labelpad=8)
    ax.set_ylabel(ylabel_left, fontsize=11, color=axis_color_left, labelpad=8)
    ax.tick_params(axis='x', rotation=0, colors="#6B7280", length=0)
    ax.tick_params(axis='y', labelcolor=axis_color_left, length=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color("#E5E7EB")
    ax.grid(True, axis='y', linestyle='-', alpha=0.5, color="#E5E7EB")
    ax.grid(False, axis='x')


def fig_to_base64(fig):
    import io, base64
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')